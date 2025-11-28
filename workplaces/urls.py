from django.urls import path
from . import views

app_name = "workplaces"

urlpatterns = [
    path("", views.WorkplacesListView.as_view(), name="list"),
    path("create/", views.WorkplaceCreateHTMXView.as_view(), name="create"),
    path("<int:pk>/update/", views.WorkplaceUpdateHTMXView.as_view(), name="update"),
    path("<int:pk>/delete/", views.WorkplaceDeleteHTMXView.as_view(), name="delete"),
    path("workplace-search", views.WorkplaceSearchHTMXView.as_view(), name="search"),
    path("task-status/<str:task_id>/", views.task_status, name="task_status"),
    # Отслеживаем статус задачи отправки уведомлений
    path("department/", views.DepartmentListView.as_view(), name="department_list"),
    path("dptreactview/", views.DepartmentReactView.as_view(), name="dpt_react_list"),
    path("staff/", views.StaffListView.as_view(), name="staff_list"),
]
