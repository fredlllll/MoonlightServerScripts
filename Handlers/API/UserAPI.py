import logging

from Framework.API.NamedAPI import NamedAPI
from Framework.API.APIMethodDecorators import require_logged_in

logger = logging.getLogger(__name__)


class UserAPI(NamedAPI):
    def __init__(self):
        super().__init__('user')

    @require_logged_in
    def get_credits(self, handler):
        return handler.current_user.get_credits(0)
