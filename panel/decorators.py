from django.http import HttpResponse


def permission_check(permission):
    def func_decorator(func):
        def wrapper(*args, **kwargs):
            if not args[0].user.has_perm(permission):
                return HttpResponse("Sorry, you don't have enough rights")
            return func(*args, **kwargs)
        return wrapper
    return func_decorator
