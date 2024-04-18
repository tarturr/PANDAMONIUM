import functools

from pandamonium.security import set_security_error


def requires(func):
    @functools.wraps(func)
    def wrapper(**kwargs):
        for key in kwargs:
            value = kwargs[key]
            error_msg = func(**kwargs)

            if error_msg:
                set_security_error(error_msg)
                return False

        return True

    return wrapper
