from rts.logger import *

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
