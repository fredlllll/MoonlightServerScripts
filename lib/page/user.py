import logging
from sanic.response import html, redirect
from lib.jinja_templates import get_template
from lib.db.models.user import User
from lib.responses import response_404, response_403
from datetime import datetime
import time

logger = logging.getLogger(__name__)


async def user(request, user_id):
    if not request.ctx.has_permission('admin'):
        return response_403(request)
    usr = User.find(user_id)
    if usr is None:
        return response_404(request)

    if usr.activation_timestamp:
        dt = datetime.fromtimestamp(usr.activation_timestamp)
        usr.activation_timestamp_str = str(dt)
    else:
        usr.activation_timestamp_str = 'False'

    template = get_template("user.html", request)
    return html(template.render(user=usr))


async def user_post(request, user_id):
    if not request.ctx.has_permission('admin'):
        return response_403(request)
    usr = User.find(user_id)
    if usr is None:
        return response_404(request)

    args = request.form
    action = args.get('action', None)
    if action == 'set-permissions':
        perms = [p.strip() for p in args.get('permissions', '').split(',')]
        if user_id == request.ctx.user.id and 'admin' not in perms:
            return redirect(f'/users/{user_id}?error=cant remove your own admin permission')
        usr.permissions = perms
        usr.save()
    elif action == 'activate':
        if not usr.activation_timestamp:
            usr.activation_timestamp = time.time()
            usr.save()
    else:
        pass

    return redirect(f'/users/{user_id}')
