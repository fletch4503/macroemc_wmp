from celery import current_app
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormMixin
from django.urls import (
    reverse_lazy,
    # reverse,
)
from django_htmx.http import HttpResponseClientRefresh
from django_htmx.middleware import HtmxDetails
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpRequest,
)
from django.views.decorators.http import require_GET
from django.template.loader import render_to_string
from .models import Workplaces, Department, Staff
from .forms import WorkplacesForm, DepartmentForm, StaffForm, SearchForm
from .tasks import create_wp_task
from celery.result import AsyncResult
from macroemc_wmp.celery import app as celery_app
from macroemc_wmp.utils import log
from django.db.models import Q
import time
import json

count_status = 0


def counter(func):
    global count_status
    count_status = 0

    def wrapper(*args, **kwargs):
        wrapper.count_status += 1  # Увеличиваем счётчик при каждом вызове функции
        log.info(f"Функция {func.__name__} была вызвана {wrapper.count_status} раз(а)")
        return func(*args, **kwargs)

    wrapper.count_status = 0  # Инициализируем счётчик
    return wrapper


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


class WorkplacesListView(FormMixin, ListView):
    model = Workplaces
    template_name = "workplaces/index.html"
    context_object_name = "workplaces"
    form_class = WorkplacesForm
    success_url = reverse_lazy("workplaces:list")
    ordering = ["-id"]
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(archived=False)
        status = self.request.GET.get("status")
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(name__icontains=query)
            log.info(
                "Передаем в index.html статус: %s и набор длиной: %s",
                status,
                len(queryset),
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.request.session.pop("task_id", None)
        task_id = self.request.session.get("task_id")
        context["form"] = self.get_form()
        context["task_id"] = task_id
        # context["search_form"] = SearchForm(self.request.GET)
        log.info("Передаем в index.html task_id: %s", task_id)
        return context

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         workplace = form.save()
    #         try:
    #             task = create_wp_task.delay(workplace.id)
    #         except Exception as e:
    #             log.error("Не получили результата из Celery c ошибкой: %s", e)
    #         res = AsyncResult(task, app=current_app)
    #         request.session["task_id"] = task.id
    #         request.session["wp_id"] = workplace.id
    #         request.session["status"] = res.state
    #         request.session["task_result"] = 1
    #         context = {
    #             "task_id": task.id,
    #             "wp": workplace,
    #             "wp_id": workplace.id,
    #             "status": "Отправляем уведомления",
    #             # "HX-Trigger": "create_run",
    #         }
    #         log.warning("Передаем в форму контекст %s", context)
    #         response = render(
    #             request,
    #             self.template_name,
    #             context,
    #         )
    #         # response["HX-Trigger"] = "create_run"
    #         log.info("Выходим из FormValid")
    #         return HttpResponseClientRefresh()
    #         # return response
    #         # html = render_to_string("workplaces/partials/wp_row.html", context)
    #         # return JsonResponse({"html": html})
    #     else:
    #         html = render_to_string(
    #             "workplaces/partials/wp_form.html", {"form": form}, request=request
    #         )
    #         return JsonResponse({"html": html}, status=400)


class WorkplaceUpdateHTMXView(UpdateView):
    model = Workplaces
    form_class = WorkplacesForm
    template_name = "workplaces/partials/wp_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        context["wp"] = self.object
        return context

    def form_valid(self, form):
        form.save()
        context = {"wp": self.object}
        row_html = render_to_string(
            "workplaces/partials/wp_row.html", context, request=self.request
        )
        # return JsonResponse({"html": html})
        # HTML формы в режиме создания
        form_context = {"form": WorkplacesForm(), "is_update": False}
        form_html = render_to_string(
            self.template_name, form_context, request=self.request
        )
        response = HttpResponse(form_html)
        # Триггер для замены строки
        response["HX-Trigger"] = json.dumps(
            {"replace-row": {"pk": self.object.pk, "html": row_html}}
        )
        return response

    def form_invalid(self, form):
        html = render_to_string(
            self.template_name,
            {"form": form, "wp": self.object, "is_update": True},
            request=self.request,
        )
        # return JsonResponse({"html": html}, status=400)
        return HttpResponse(html, status=400)


class WorkplaceDeleteHTMXView(DeleteView):
    model = Workplaces

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        wp = get_object_or_404(Workplaces, pk=self.kwargs["pk"])
        log.warning("Soft-удаление элемента %s", wp.name)
        wp.archived = True
        wp.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "wp-deleted"
        # self.object.delete()
        return response


class WorkplaceSearchHTMXView(ListView):
    model = Workplaces
    template_name = "workplaces/wp_list.html"

    def get(self, request, *args, **kwargs):
        time.sleep(1)
        # qs = super().get_queryset()
        query = request.GET.get("search", default="")
        log.warning("Ищем строку: %s", query)
        wp = Workplaces.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(department__name__icontains=query)
            | Q(department__staff__last_name__icontains=query),
            archived=False,
        )
        return render(request, "workplaces/wp_list.html", {"workplaces": wp})


class DepartmentListView(FormMixin, ListView):
    model = Department
    template_name = "workplaces/dpt_list.html"
    context_object_name = "departments"
    form_class = DepartmentForm
    ordering = ["-id"]
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["search_form"] = SearchForm(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            department = form.save()
            context = {"department": department}
            html = render_to_string("workplaces/partials/dpt_row.html", context)
            return JsonResponse({"html": html})
        else:
            html = render_to_string(
                "workplaces/partials/department_form.html",
                {"form": form},
                request=request,
            )
            return JsonResponse({"html": html}, status=400)


class StaffListView(FormMixin, ListView):
    model = Staff
    template_name = "workplaces/staff_list.html"
    context_object_name = "staffs"
    form_class = StaffForm
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(first_name__icontains=query) | queryset.filter(
                last_name__icontains=query
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["search_form"] = SearchForm(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            staff = form.save()
            context = {"staff": staff}
            html = render_to_string("workplaces/partials/staff_row.html", context)
            return JsonResponse({"html": html})
        else:
            html = render_to_string(
                "workplaces/partials/staff_form.html", {"form": form}, request=request
            )
            return JsonResponse({"html": html}, status=400)


class WorkplaceCreateHTMXView(CreateView):
    """
    Создаем новое рабочее место
    """

    model = Workplaces
    form_class = WorkplacesForm
    template_name = "workplaces/partials/wp_row.html"
    success_url = reverse_lazy("workplaces:list")

    def form_valid(self, form):
        self.request.session.pop("task_id", None)  # Сбрасываем задачу
        response = super().form_valid(form)
        context = self.get_context_data(form=form)
        wp = self.object
        wp_id = self.object.id
        log.info(
            "Form is valid, creating workplace: %s and context: %s", wp_id, context
        )
        try:
            task = create_wp_task.delay(wp_id)
        except Exception as e:
            log.error("Не получили результата из Celery c ошибкой: %s", e)
        res = AsyncResult(task.id, app=current_app)
        self.request.session["task_id"] = task.id
        self.request.session["wp_id"] = wp_id
        self.request.session["wp"] = wp
        self.request.session["status"] = res.state
        self.request.session["task_result"] = 1
        context = {
            "task_id": task.id,
            "wp": wp,
            "wp_id": wp_id,
            "status": "Отправляем уведомления",
            # "HX-Trigger": "create_run",
        }
        log.warning("Передаем в форму контекст %s", context)
        response = render(
            self.request,
            self.template_name,
            context,
        )
        # response["HX-Trigger"] = "create_run"
        log.info("Выходим из FormValid")
        return HttpResponseClientRefresh()


@counter
@require_GET
def task_status(request: HtmxHttpRequest, task_id) -> HttpResponse:
    """
    Отображаем статус отправки уведомлений сотрудникам отдела после создания рабочего места
    """
    global count_status
    count_status += 1
    task_id = request.GET.get("task_id") or task_id
    wp_id = request.session.get("wp_id")
    extstatus = request.session.get("status")
    template_name = "worplaces/partials/task_status.html#task-status-info"
    # url = reverse("workplaces:task_status")
    res = AsyncResult(task_id, app=current_app)
    if request.htmx:
        log.warning(
            "Итерация %s, task_id: %s, Ext_Status: %s, Task Status: %s",
            count_status,
            task_id,
            extstatus,
            res.state,
        )
    context = {
        "task_id": task_id,
        "wp_id": wp_id,
        "task_result": count_status,
        "status": "Отправляем уведомления",
    }
    response = render(request, template_name=template_name, context=context)
    if res.state == "SUCCESS":
        count_status = 0
        context["status"] = "SUCCESS"
        response = render(request, template_name=template_name, context=context)
        response["HX-Trigger"] = "success"
        # Очищаем task_id и lesson_id из сессии когда задача завершена
        request.session.pop("task_id", None)
        request.session.pop("wp_id", None)
        log.warning("Текущий статус: %s и контекст: %s", res.state, context)
        return HttpResponseClientRefresh()
    elif res.state == "FAILURE":
        count_status = 0
        context["status"] = "FAILURE"
        response = render(request, template_name=template_name, context=context)
        response["HX-Trigger"] = "failure"
        # Очищаем task_id и wp_id из сессии при ошибке
        request.session.pop("task_id", None)
        request.session.pop("wp", None)
        log.warning("Текущий статус: %s и контекст: %s", res.state, context)
        return HttpResponseClientRefresh()
    else:
        response = render(request, template_name=template_name, context=context)
        log.warning("Отправляем в форму контекст %s", context)
        return response
