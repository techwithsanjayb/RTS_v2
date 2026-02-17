from rts.logger import *

def redirect_based_on_role(user):
    if user.groups.filter(name="PortalAdmin").exists():
        return "core:administrator_dashboard"

    elif user.groups.filter(name="Agents").exists():
        return "core:agent_dashboard"

    elif user.groups.filter(name="User").exists():
        return "core:user_dashboard"

    return None
