from sanic.response import json, HTTPResponse


def response_404(message=None) -> HTTPResponse:
    return json({
        'status': 404,
        'message': message or f"Could not find resource"
    }, status=404)


def response_403(message=None) -> HTTPResponse:
    return json({
        'status': 403,
        'message': message or "Access Denied"
    }, status=403)


def response_list(lst) -> HTTPResponse:
    return json({
        'status': 200,
        'items': lst
    })


def response_one(item) -> HTTPResponse:
    return json({
        'status': 200,
        'item': item
    })


def response_err(message) -> HTTPResponse:
    return json({
        'status': 500,
        'message': message
    }, status=500)
