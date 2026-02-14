from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

#########################################################################

User = get_user_model()

#########################################################################
'''
1 - Railway Catering
2 - IT Supoort
3 - User Ticketing System  
'''

class System(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "system"
        ordering = ["name"]
        verbose_name = _("System")
        verbose_name_plural = _("Systems")

    def __str__(self):
        return self.name

##############################################################################

'''
Western
Eastern
Southern
'''
class Zone(models.Model):
    system = models.ForeignKey(
        System,
        on_delete=models.PROTECT,
        related_name="zones"
    )

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "zone"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["system", "name"],
                name="unique_zone_per_system"
            ),
            models.UniqueConstraint(
                fields=["system", "code"],
                name="unique_zone_code_per_system"
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


#####################################################################
'''
Mumbai
Pune
Nasik
'''
class Division(models.Model):
    zone = models.ForeignKey(
        Zone,
        on_delete=models.PROTECT,
        related_name="divisions"
    )

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "division"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["code"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["zone", "name"],
                name="unique_division_per_zone"
            ),
            models.UniqueConstraint(
                fields=["zone", "code"],
                name="unique_division_code_per_zone"
            ),
        ]

    def __str__(self):
        return f"{self.name} - {self.zone.name}"


############################################################################################
'''
Rolling Stock
Fixed Infrastructire
'''
class Department(models.Model):
    division = models.ForeignKey(
        "Division",
        on_delete=models.PROTECT,
        related_name="departments"
    )

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
        constraints = [
            models.UniqueConstraint(
                fields=["division", "name"],
                name="unique_department_per_division"
            ),
            models.UniqueConstraint(
                fields=["division", "code"],
                name="unique_department_code_per_division"
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.division.name})"



############################################################
'''
LHB
ICF
'''
class Coach_Type(models.Model):
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
Coach Related
Track Related
Engine Related
'''
class Category(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="categories"
    )
    coach = models.ForeignKey(
        Coach_Type,
        on_delete=models.PROTECT,
        related_name="coach",
        )

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["department", "name"],
                name="unique_category_per_department"
            ),
            models.UniqueConstraint(
                fields=["department", "code"],
                name="unique_category_code_per_department"
            ),
        ]

    def __str__(self):
        return f"{self.name} - {self.department.name}"

##################################################
'''
Electrical Dept
Electrical/AC
Mechanical (C&W)
Mechanical (C&W)
'''
class ResponsibleUnit(models.Model):
    unit_name = models.CharField(max_length=150, unique=True)
    short_code = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "responsible_unit"
        ordering = ["unit_name"]

    def __str__(self):
        return self.unit_name


########################################################
'''
Electrical 
AC
Brakes
Passenger
'''
class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="subcategories"
    )

    responsible_unit = models.ForeignKey(
        ResponsibleUnit,
        on_delete=models.PROTECT,
        related_name="subcategories"
    )

    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subcategory"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_subcategory_per_category"
            ),
            models.UniqueConstraint(
                fields=["category", "code"],
                name="unique_subcategory_code_per_category"
            ),
        ]

    def __str__(self):
        return f"{self.name} - {self.category.name}"

########################################################

'''
JE Electrical
SSE AC
DIVISION CONTROL
AGENT
'''
class OfficerRole(models.Model):
    role_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.role_name

########################################################
'''
ASHWINI -- IAS
DIVYA -- IPS
SANJAY -- AGENT
'''

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    officer_role = models.ForeignKey(OfficerRole, on_delete=models.SET_NULL, null=True)
    responsible_unit = models.ForeignKey(ResponsibleUnit, on_delete=models.SET_NULL, null=True)

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
class Issue(models.Model):

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.PROTECT,
        related_name="issues"
    )

    officer_role = models.ForeignKey(
        OfficerRole,
        on_delete=models.PROTECT
    )

    name = models.CharField(max_length=150)
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
    issue = models.ForeignKey(Issue, on_delete=models.PROTECT)
    raised_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="raised_tickets"
    )
    assigned_responsible_unit  = models.ForeignKey(
        ResponsibleUnit,
        on_delete=models.PROTECT,
        related_name="unit_tickets"
    )
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
