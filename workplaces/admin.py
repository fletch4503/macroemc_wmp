from django.contrib import admin
from workplaces.models import Workplaces, Department, Staff

# Register your models here.
@admin.register(Workplaces)
class WorkplacesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "type",
        "department",
        "ip",
        "mac",
        "archived",
    )
    list_filter = (
        "id",
        "name",
        "description",
        "type",
        "department",
        "ip",
        "mac",
        "archived",
    )

    def visible(self, obj: Workplaces) -> bool:
        return not obj.archived

    visible.boolean = True


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "archived",
    )

    def visible(self, obj: Department) -> bool:
        return not obj.archived

    visible.boolean = True

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "department",
        "email",
        "phone",
        "archived",
    )

    def visible(self, obj: Staff) -> bool:
        return not obj.archived

    visible.boolean = True