from rts.logger import *
from .models import Ticket, TicketStatus, Department, List_of_Issue, Resolver
from django.utils import timezone
from django.db.models import Q, Count
import uuid

def redirect_based_on_role(user):
    record("Inside redirect_based_on_role function")
    
    if user.groups.filter(name="PortalAdmin").exists():
        record("Role is Portal Admin")
        return "core:administrator_dashboard"

    elif user.groups.filter(name="ResolverUnit").exists():
        record("Role is Resolver")
        return "core:resolver_dashboard"

    elif user.groups.filter(name="RaiserUnit").exists():
        record("Role is Raiser")
        return "core:raiser_dashboard"

    return None

##########################################################
def generate_complaint_id():
    """Generates a unique ID like TIC-A1B2C3D4."""
    return f"TIC-{uuid.uuid4().hex[:8].upper()}"

##########################################################

from django.db.models import Count, Q
from django.utils import timezone



def auto_assign_ticket(ticket):
    try:
        target_issue = ticket.issue
    except AttributeError:
        return None

    # Use 'assigned_tickets' as it appears in your 'Choices'
    # Use 'status__code' (or similar) to avoid the property error
    resolver_qs = Resolver.objects.filter(issue=target_issue).annotate(
        active_load=Count(
            'assigned_tickets', 
            filter=~Q(assigned_tickets__status__code='CLOSED')
        )
    )

    # Order: Priority to those NOT busy, then lowest load, then Round Robin
    best_resolver = resolver_qs.order_by('is_busy', 'active_load', 'last_assigned_at').first()

    if best_resolver:
        ticket.issue_resolver_name = best_resolver
        print('Best resolver value print',best_resolver)
        
        # Using 'responsible_dept' from your error's choice list
        if hasattr(best_resolver, 'responsible_dept'):
            ticket.assigned_responsible_unit = best_resolver.responsible_dept
        
        # Update resolver metadata
        best_resolver.last_assigned_at = timezone.now()
        best_resolver.is_busy = True 
        best_resolver.save()
        
        return best_resolver
        
    return None