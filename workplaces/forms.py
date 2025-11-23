from django import forms
from .models import Workplaces, Department, Staff


class WorkplacesForm(forms.ModelForm):
    class Meta:
        model = Workplaces
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control-wide", "style": "width: 400px;"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control-wide",
                    "rows": "2",
                    "cols": "30",
                    "style": "width: 400px;",
                }
            ),
            "type": forms.Select(
                attrs={"class": "form-control-wide", "style": "width: 400px;"}
            ),
            "department": forms.Select(
                attrs={"class": "form-control-wide", "style": "width: 400px;"}
            ),
            "ip": forms.TextInput(
                attrs={
                    "class": "form-control-wide",
                    "style": "width: 400px;",
                    "placeholder": "192.168.001.001",
                    # "maxlength": 15,  # IPv4 max length
                    "pattern": r"^(\d{1,3}\.){3}\d{1,3}$",  # простая проверка паттерна (не строгая)
                }
            ),
            "mac": forms.TextInput(
                attrs={
                    "class": "form-control-wide",
                    "style": "width: 400px;",
                    "placeholder": "AA:BB:CC:DD:EE:FF",
                    "maxlength": 17,
                    "pattern": r"^([0-9A-Fa-f]{2}[:\-]){5}([0-9A-Fa-f]{2})$",
                }
            ),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name", "description"]


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["first_name", "last_name", "department", "email", "phone"]


class SearchForm(forms.Form):
    query = forms.CharField(required=False, label="Поиск")
