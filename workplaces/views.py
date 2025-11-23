from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import (
    # reverse_lazy,
    reverse,
)
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .models import Workplaces, Department, Staff
from .forms import WorkplacesForm, DepartmentForm, StaffForm, SearchForm
from .tasks import process_workplace_creation
from celery.result import AsyncResult
from macroemc_wmp.utils import log
from django.db.models import Q
import time
# import workplaces
# from django.contrib import messages


class WorkplacesListView(FormMixin, ListView):
    model = Workplaces
    template_name = "workplaces/index.html"
    context_object_name = "workplaces"
    form_class = WorkplacesForm
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
            workplace = form.save()
            task = process_workplace_creation.delay(workplace.id)
            request.session["task_id"] = task.id
            context = {"workplace": workplace}
            html = render_to_string("workplaces/partials/wp_row.html", context)
            return JsonResponse({"html": html})
        else:
            html = render_to_string(
                "workplaces/partials/wp_form.html", {"form": form}
            )
            return JsonResponse({"html": html}, status=400)


class WorkplaceUpdateHTMXView(UpdateView):
    model = Workplaces
    form_class = WorkplacesForm
    template_name = "workplaces/partials/wp_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        context['wp'] = self.object
        return context

    def form_valid(self, form):
        form.save()
        context = {"wp": self.object}
        row_html = render_to_string("workplaces/partials/wp_row.html", context)
        # return JsonResponse({"html": html})
        # HTML формы в режиме создания
        form_context = {"form": WorkplacesForm(), "is_update": False}
        form_html = render_to_string(self.template_name, form_context)
        response = HttpResponse(form_html)
        # Триггер для замены строки
        response["HX-Trigger"] = json.dumps({"replace-row": {"pk": self.object.pk, "html": row_html}})
        return response


    def form_invalid(self, form):
        html = render_to_string(
            self.template_name, {"form": form, "wp": self.object, "is_update": True}
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
        query=request.GET.get("search", default='')
        log.warning("Ищем строку: %s",query)
        wp = Workplaces.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(department__name__icontains=query)
            | Q(department__staff__last_name__icontains=query)
        )
        return render(
            request, "workplaces/wp_list.html",{"workplaces": wp}
        )

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
                "workplaces/partials/department_form.html", {"form": form}
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
                "workplaces/partials/staff_form.html", {"form": form}
            )
            return JsonResponse({"html": html}, status=400)


def task_status(request):
    task_id = request.session.get("task_id")
    url = reverse("workplaces:task_status")
    if task_id:
        result = AsyncResult(task_id)
        status = result.status
        if status == "PENDING":
            response = "Задача в очереди..."
            html = f'<div id="task-status" hx-get="{url}" hx-trigger="every 5s"><p>Статус задачи: {response}</p></div>'
        elif status == "SUCCESS":
            response = "Задача завершена успешно."
            html = f'<div id="task-status"><p>Статус задачи: {response}</p></div>'
        elif status == "FAILURE":
            response = "Задача завершилась с ошибкой."
            html = f'<div id="task-status"><p>Статус задачи: {response}</p></div>'
        else:
            response = f"Статус: {status}"
            html = f'<div id="task-status"><p>Статус задачи: {response}</p></div>'
    else:
        response = "Нет активной задачи."
        html = f'<div id="task-status"><p>Статус задачи: {response}</p></div>'
    return HttpResponse(html)
