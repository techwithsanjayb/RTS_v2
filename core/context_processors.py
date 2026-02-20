def user_roles(request):
    if request.user.is_authenticated:
        return {
            "is_portal_admin": request.user.groups.filter(name="PortalAdmin").exists(),
            "is_agent": request.user.groups.filter(name="Agents").exists(),
            "is_user": request.user.groups.filter(name="User").exists(),
        }
    return {}