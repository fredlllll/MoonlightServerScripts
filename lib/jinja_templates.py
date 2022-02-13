from jinja2 import Environment, FileSystemLoader


async def get_template(name, request):
    env = Environment(loader=FileSystemLoader('templates'))
    user = request.ctx.user

    def has_permission(perm):
        if request.ctx.user is not None:
            return request.ctx.user.has_permission(perm)

    # add anything you want available in all template files into the globals dict

    t = env.get_template(name, globals={
        'user': user,
        'has_permission': has_permission,
    })
    return t
