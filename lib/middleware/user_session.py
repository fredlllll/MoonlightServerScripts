from lib.settings import Settings
from lib.db.models.session import Session
from lib.db.models.user import User


async def user_session(request):
    request.ctx.user = None
    request.ctx.session = None

    session_id = request.cookies.get(Settings.session_cookie_name, None)
    if session_id is None:
        return
    sess = await Session.find(session_id)
    if sess is None:
        return

    request.ctx.session = sess
    request.ctx.user = await User.find(sess.user_id)
