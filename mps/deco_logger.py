from functools import wraps


def deco_logger(log, length=None):
    length = 10 if length is None else length
    def log_function(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            log.info(u"{} args:{}, kwargs:{}".format(
                f.__name__,
                u','.join([unicode(arg)[0:length] for arg in args]),
                u','.join([unicode(arg)[0:length] for arg in kwargs]),
                ), extra={
                    'funcname_override': f.__name__,
                })
            return f(*args, **kwargs)

        return wrapped

    return log_function
