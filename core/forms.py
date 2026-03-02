from django import forms
from datetime import timezone
from core.models import Ticket, TicketStatus, Department, Category, coach_type as CoachType, List_of_Issue

class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=True,
        label="User name",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter username',
                'class':'form-control'
                }
            )
    )

    password = forms.CharField(
        max_length=20,
        required=True,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password',
                'class':'form-control'
                }
        )
    )
#########################################################################

class TicketCreateForm(forms.ModelForm):
    """Form for raisers. Includes dependent dropdowns:
    Department -> Category -> Issue
    """

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_department'}),
        required=True,
        label="Department",
        empty_label="-- Select Department --"
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
        required=True,
        label="Category",
        empty_label="-- Select Category --"
    )
    
    issue = forms.ModelChoiceField(
        queryset=List_of_Issue.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_issue'}),
        required=True,
        label="Issue",
        empty_label="-- Select Issue --"
    )
    
    

    class Meta:
        model = Ticket
        fields = ['issue', 'user_description']
        widgets = {
            'user_description': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5,
                'placeholder': 'Please describe the issue in detail',
                'id': 'id_user_description'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If form is bound and department is selected, filter categories
        if 'department' in self.data:
            try:
                dept_id = int(self.data.get('department'))
                self.fields['category'].queryset = Category.objects.filter(department_id=dept_id)
                # If category is also selected, filter issues
                if 'category' in self.data:
                    cat_id = int(self.data.get('category'))
                    self.fields['issue'].queryset = List_of_Issue.objects.filter(Issue_category_id=cat_id)
            except (ValueError, TypeError):
                pass

    def save(self, commit=True, raised_by=None):
        ticket = super().save(commit=False)
        if raised_by:
            ticket.raised_by = raised_by
        # ticket.reported_date = timezone.now()
        ticket.status = TicketStatus.objects.filter(code='OPEN').first()
        if commit:
            ticket.save()
        return ticket
