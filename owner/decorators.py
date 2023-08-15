from django.shortcuts import redirect
def deco_login(fun):
    def wrapper(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return fun(self, request, *args, **kwargs)
        return redirect('/login')
    return wrapper
