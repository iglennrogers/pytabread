import logging

import falcon

import functools


def logger(source):
    return logging.getLogger("pytabread." + source)


def trace_scope(tag: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger(func.__module__).info("Enter:" + tag)
            ret = func(*args, **kwargs)
            logger(func.__module__).info("Leave:" + tag)
            return ret
        return wrapper
    return decorator


def dump_context():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            req = find_arg(falcon.Request, args)
            logger(func.__module__).info("Request:" + str(req.context["json"]))
            ret = func(*args, **kwargs)
            resp = find_arg(falcon.Response, args)
            logger(func.__module__).info("Response:" + str(resp.body))
            return ret
        return wrapper
    return decorator


def find_arg(cls, args):
    for arg in args:
        if isinstance(arg, cls):
            return arg
    return None
