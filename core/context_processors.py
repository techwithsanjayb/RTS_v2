def user_roles(request):
    if request.user.is_authenticated:
        return {
            "is_portal_admin": request.user.groups.filter(name="PortalAdmin").exists(),
            "is_resolver": request.user.groups.filter(name="ResolverUnit").exists(),
            "is_raiser": request.user.groups.filter(name="RaiserUnit").exists(),
        }
    return {}