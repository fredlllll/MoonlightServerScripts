from models.User import *
from passlib.apps import custom_app_context
import logging

logger = logging.getLogger(__name__)


def hash_password(password):
    return custom_app_context.hash(password)


def verify_password(password, hash):
    return custom_app_context.verify(password, hash)
