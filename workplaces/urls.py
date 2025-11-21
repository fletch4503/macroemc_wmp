from django.urls import path
from . import views

app_name = "workplaces"

urlpatterns = [
    path("", views.WorkplacesListView.as_view(), name="list"),
    path("<int:pk>/update/", views.WorkplaceUpdateHTMXView.as_view(), name="update"),
    path("<int:pk>/delete/", views.WorkplaceDeleteHTMXView.as_view(), name="delete"),
    path("task-status/", views.task_status, name="task_status"),
    path("department/", views.DepartmentListView.as_view(), name="department_list"),
    path(
        "department/<int:pk>/update/",
        views.DepartmentUpdateHTMXView.as_view(),
        name="department_update",
    ),
    path(
        "department/<int:pk>/delete/",
        views.DepartmentDeleteHTMXView.as_view(),
        name="department_delete",
    ),
    path("staff/", views.StaffListView.as_view(), name="staff_list"),
    path(
        "staff/<int:pk>/update/",
        views.StaffUpdateHTMXView.as_view(),
        name="staff_update",
    ),
    path(
        "staff/<int:pk>/delete/",
        views.StaffDeleteHTMXView.as_view(),
        name="staff_delete",
    ),
]
