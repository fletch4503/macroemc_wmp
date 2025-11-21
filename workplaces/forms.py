from django import forms
from .models import Workplaces, Department, Staff


class WorkplacesForm(forms.ModelForm):
    class Meta:
        model = Workplaces
        fields = ["name", "description", "type", "department", "ip", "mac"]


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
