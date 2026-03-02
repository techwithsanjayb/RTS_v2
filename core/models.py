from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

######################################################################
'''
Electrical Dept
Electrical/AC
Mechanical (C&W)
Mechanical (C&W)
'''
class Department(models.Model):

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)

    sla_hours = models.PositiveIntegerField(
        help_text="Default SLA in hours for this department"
    )

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "department"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return f"{self.name}"

############################################################
'''
Electrical 
AC
Brakes
Passenger

'''
class Category(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="categories"
    )

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category"
        ordering = ["name"]
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["department", "name"],
        #         name="unique_category_per_department"
        #     ),
        #     models.UniqueConstraint(
        #         fields=["department", "code"],
        #         name="unique_category_code_per_department"
        #     ),
        # ]

    def __str__(self):
        return f"{self.name} - {self.department.name}"


############################################################
'''
LHB
ICF
'''
class coach_type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Coach_Type"
        ordering = ["name"]

    def __str__(self):
        return self.name
       
############################################################

'''
JE Electrical
SSE AC
DIVISION CONTROL
AGENT
'''
class Officer_Role(models.Model):
    name = models.CharField(max_length=150)
    officer_department = models.ForeignKey(Department, on_delete=models.CASCADE)

########################################################


########################################################


########################################################
'''
ASHWINI -- IAS
DIVYA -- IPS
SANJAY -- AGENT
'''

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    officer_role = models.ForeignKey(Officer_Role, on_delete=models.SET_NULL, null=True)
    responsible_dept = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username
    
########################################################
'''
Level-2
Level-1
Immediate
'''    
class EscalationLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    priority_order = models.PositiveIntegerField()

    def __str__(self):
        return self.name


#########################################################
'''
Light NOt working
Brake issues 
Door issues
'''
class List_of_Issue(models.Model):

    name = models.CharField(max_length=150)
    Issue_category = models.ForeignKey(Category,on_delete=models.PROTECT)
    code = models.CharField(max_length=50)

    severity = models.CharField(max_length=20)
    sla_hours = models.PositiveIntegerField()
    escalation_level = models.ForeignKey(
        EscalationLevel,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name

########################################################
'''
Open
On Hold
In process
Completed
Invalid

'''

class TicketStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    sequence_order = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ticket_status"
        ordering = ["sequence_order"]

    def __str__(self):
        return self.name


########################################################


class Ticket(models.Model):

    complaint_id = models.CharField(max_length=20, unique=True)
    issue = models.ForeignKey(List_of_Issue, on_delete=models.PROTECT)
    raised_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="raised_tickets"
    )

    assigned_responsible_unit  = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="unit_tickets"
    )
    issue_resolver_name = models.ForeignKey(UserProfile,on_delete=models.PROTECT)
    user_description = models.TextField()
    resolution_description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(
    TicketStatus,
    on_delete=models.PROTECT,
    related_name="tickets"
)
    reported_date = models.DateTimeField()
    resolved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.complaint_id

########################################################
