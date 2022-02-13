from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.user import User
from lib.db.models.session import Session


async def login(request):
    template = await get_template('login.html', request)
    return html(template.render())


async def login_post(request):
    user_name = request.form.get("user")
    password = request.form.get("password")
    user = await User.authenticate_user(user_name, password)  # either false or user object
    if user:  # login worked
        session = Session(user_id=user.id)
        await session.save()
        response = redirect('/')
        session.set_cookie(response)
        return response
    return redirect('/login')


async def logout(request):
    resp = redirect('/')
    Session.clear_cookie(resp)
    await request.ctx.session.delete()
    return resp
