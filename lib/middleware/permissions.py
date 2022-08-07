async def permissions(request):
    if request.ctx.user is None:
        def has_permission_false(_):
            return False

        request.ctx.has_permission = has_permission_false
    else:
        def has_permission(perm):
            return request.ctx.user.has_permission(perm)

        request.ctx.has_permission = has_permission
