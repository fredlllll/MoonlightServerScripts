from lib.jinja_templates import get_template
from sanic.response import html


def response_404(request, message: str = None):
    template = get_template('404.html', request)
    return html(template.render(message=message), status=404)
