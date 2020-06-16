from functools import wraps


# def tags(tag_name):
#    def tags_decorator(func):
#        @wraps(func)
#        def func_wrapper(name):
#            return "<{0}>{1}</{0}>".format(tag_name, func(name))
#
#        return func_wrapper
#
#    return tags_decorator


def require_logged_in(func):
    def tmp(*args, **kwargs):
        slf = args[1]
        if slf.current_user is not None:
            return func(*args, **kwargs)
        else:
            return slf.do_403()

    return tmp


def require_permission(permission):
    @require_logged_in
    def tmp_decorator(func):
        @wraps(func)
        def tmp(*args, **kwargs):
            slf = args[1]
            if slf.current_user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return slf.do_403()

        return tmp

    return tmp_decorator
