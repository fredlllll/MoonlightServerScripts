from sanic.response import redirect


async def logged_in(request):
    if request.ctx.user is None:
        return redirect('/login')


async def logged_out(request):
    if request.ctx.user is not None:
        return redirect('/')
