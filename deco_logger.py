
def deco_logger(log, length=None):
    length = 10 if length is None else length
    def log_function(f):
        def wrapped(*args, **kwargs):
            log.info(u"{} args:{}, kwargs:{}".format(
                f.__name__,
                u','.join([str(arg)[0:length] for arg in args]),
                u','.join([str(arg)[0:length] for arg in kwargs]),
                ))
            return f(*args, **kwargs)

        return wrapped

    return log_function
