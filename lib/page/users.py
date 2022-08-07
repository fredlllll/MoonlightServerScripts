import logging
from sanic.response import html
from lib.jinja_templates import get_template
from lib.db.models.user import User
from lib.responses import response_403
from datetime import datetime

logger = logging.getLogger(__name__)


async def users(request):
    if not request.ctx.has_permission('admin'):
        return response_403(request)
    users_ = User.all()
    for u in users_:
        if u.activation_timestamp:
            dt = datetime.fromtimestamp(u.activation_timestamp)
            u.activation_timestamp_str = str(dt)
        else:
            u.activation_timestamp_str = 'False'
    template = get_template("users.html", request)
    return html(template.render(users=users_))
