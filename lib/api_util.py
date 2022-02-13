from sanic.response import json


def response_404(message=None):
    return json({
        'status': 404,
        'message': message or f"Could not find resource"
    }, status=404)


def response_403(message=None):
    return json({
        'status': 403,
        'message': message or "Access Denied"
    }, status=403)


def response_list(lst):
    return json({
        'status': 200,
        'items': lst
    })


def response_one(item):
    return json({
        'status': 200,
        'item': item
    })


def response_err(message):
    return json({
        'status': 500,
        'message': message
    }, status=500)
