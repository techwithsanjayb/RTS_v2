from django.contrib import admin

from .models import *
admin.site.register(Department)
admin.site.register(Category)
admin.site.register(List_of_Issue)
admin.site.register(EscalationLevel)
admin.site.register(Ticket)
admin.site.register(TicketStatus)
admin.site.register(Resolver)
admin.site.register(Officer_Role)
#     # Category,
#     # Coach_Type,
#     # Department,
#     # # Division,
#     # EscalationLevel,
#     # List_of_Issue,
#     # OfficerRole,
#     # ResponsibleUnit,
#     # SubCategory,
#     # System,
#     # Ticket,
#     # TicketStatus,
#     # UserProfile,
#     Zone,


# @admin.register(Department)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "code",
#         "division",
#         "sla_hours",
#         "is_active",
#         "created_at",
#         "updated_at",
#     )
#     list_filter = ("division", "is_active")
#     search_fields = ("name", "code", "division__name")
#     autocomplete_fields = ("division",)
#     ordering = ("name",)


# @admin.register(Coach_Type)
# class CoachTypeAdmin(admin.ModelAdmin):
#     list_display = ("name", "code", "is_active", "created_at", "updated_at")
#     list_filter = ("is_active",)
#     search_fields = ("name", "code")
#     ordering = ("name",)


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "code",
#         "department",
#         "coach",
#         "is_active",
#         "created_at",
#         "updated_at",
#     )
#     list_filter = ("department", "coach", "is_active")
#     search_fields = ("name", "code", "department__name", "coach__name")
#     autocomplete_fields = ("department", "coach")
#     ordering = ("name",)


# @admin.register(ResponsibleUnit)
# class ResponsibleUnitAdmin(admin.ModelAdmin):
#     list_display = (
#         "unit_name",
#         "short_code",
#         "is_active",
#         "created_at",
#         "updated_at",
#     )
#     list_filter = ("is_active",)
#     search_fields = ("unit_name", "short_code")
#     ordering = ("unit_name",)


# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "code",
#         "category",
#         "responsible_unit",
#         "is_active",
#         "created_at",
#         "updated_at",
#     )
#     list_filter = ("category", "responsible_unit", "is_active")
#     search_fields = (
#         "name",
#         "code",
#         "category__name",
#         "responsible_unit__unit_name",
#     )
#     autocomplete_fields = ("category", "responsible_unit")
#     ordering = ("name",)


# @admin.register(OfficerRole)
# class OfficerRoleAdmin(admin.ModelAdmin):
#     list_display = ("role_name",)
#     search_fields = ("role_name",)
#     ordering = ("role_name",)


# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ("user", "officer_role", "responsible_unit")
#     list_filter = ("officer_role", "responsible_unit")
#     search_fields = ("user__username", "officer_role__role_name", "responsible_unit__unit_name")
#     autocomplete_fields = ("user", "officer_role", "responsible_unit")


# @admin.register(EscalationLevel)
# class EscalationLevelAdmin(admin.ModelAdmin):
#     list_display = ("name", "priority_order")
#     search_fields = ("name",)
#     ordering = ("priority_order",)


# @admin.register(Issue)
# class IssueAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "code",
#         "subcategory",
#         "officer_role",
#         "severity",
#         "sla_hours",
#         "escalation_level",
#     )
#     list_filter = ("officer_role", "escalation_level", "severity")
#     search_fields = ("name", "code", "subcategory__name", "officer_role__role_name")
#     autocomplete_fields = ("subcategory", "officer_role", "escalation_level")
#     ordering = ("name",)


# @admin.register(TicketStatus)
# class TicketStatusAdmin(admin.ModelAdmin):
#     list_display = ("name", "code", "is_active", "sequence_order", "created_at")
#     list_filter = ("is_active",)
#     search_fields = ("name", "code")
#     ordering = ("sequence_order",)


# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = (
#         "complaint_id",
#         "issue",
#         "raised_by",
#         "assigned_responsible_unit",
#         "status",
#         "reported_date",
#         "resolved_at",
#         "created_at",
#         "updated_at",
#     )
#     list_filter = ("status", "assigned_responsible_unit", "reported_date", "created_at")
#     search_fields = (
#         "complaint_id",
#         "issue__name",
#         "raised_by__username",
#         "assigned_responsible_unit__unit_name",
#     )
#     autocomplete_fields = ("issue", "raised_by", "assigned_responsible_unit", "status")
#     readonly_fields = ("created_at", "updated_at")
#     ordering = ("-created_at",)
 
