from rts.logger import *

def redirect_based_on_role(user):
    record("Inside redirect_based_on_role function")
    
    if user.groups.filter(name="PortalAdmin").exists():
        record("Role is Portal Admin")
        return "core:administrator_dashboard"

    elif user.groups.filter(name="Agents").exists():
        record("Role is Agent")
        return "core:agent_dashboard"

    elif user.groups.filter(name="User").exists():
        record("Role is User")
        return "core:user_dashboard"

    return None
