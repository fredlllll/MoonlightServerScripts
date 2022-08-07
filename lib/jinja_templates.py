from jinja2 import Environment, FileSystemLoader, Template
from sanic import Request


def get_template(name: str, request: Request) -> Template:
    env = Environment(loader=FileSystemLoader('templates'))
    user = request.ctx.user

    # add anything you want available in all template files into the globals dict

    t = env.get_template(name, globals={
        'user': user,
        'has_permission': request.ctx.has_permission,
    })
    return t
