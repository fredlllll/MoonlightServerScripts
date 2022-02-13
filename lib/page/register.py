from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.user import User
from lib.util import hash_password
import time


async def register(request):
    template = await get_template('register.html', request)
    return html(template.render())


async def register_post(request):
    template = await get_template('register.html', request)

    user_name = request.form.get("user")
    password = request.form.get("password")
    password1 = request.form.get("password1")
    if password != password1:
        return html(template.render(error='passwords dont match'))

    if await User.is_user_name_taken(user_name):
        return html(template.render(error='user already exists'))

    if len(await User.all()) == 0:  # automatically activate the first user who registers
        auto_activate = True
    else:
        auto_activate = False
    user = User(name=user_name, password=hash_password(password), permissions=['admin'])
    if auto_activate:
        user.activation_timestamp = time.time()
    await user.save()
    return redirect('/login')  # to login