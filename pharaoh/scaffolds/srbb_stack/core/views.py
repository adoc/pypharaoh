

def unauthorized_view(request):
    """Return HTTPUnauthorized when user is logged in but unauthorized,
    redirect to 'login' route if no user is logged in.
    """
    # do not allow a user to login if they are already logged in
    if pyramid.security.authenticated_userid(request):
        return pyramid.httpexceptions.HTTPUnauthorized()

    return pyramid.httpexceptions.HTTPFound(location=
                request.route_url('login', _query=(('next', request.path),)))


@pyramid.view.view_config(route_name='login',
                            renderer='templates/login.html.mako')
def login_view(request):
    if 'submit' in request.POST:
        next = request.params.get('next') or request.route_url('home')
        user_name = request.POST.get('login', '')
        passwd = request.POST.get('password', '')

        user = get_user(request, user_name)
        if user and user.check_password(passwd):
            headers = pyramid.security.remember(request, user_name)
            return pyramid.httpexceptions.HTTPFound(location=next, headers=headers)
        else:
            return {'failed': True}
    return {}


# @pyramid.view.view_config(route_name='logout')
def logout_view(request):
    """Logout view removes the cookie and redirects to the
    "after_logout" route.
    """

    return pyramid.httpexceptions.HTTPFound(
                            location=request.route_url('home'),
                            headers=pyramid.security.forget(request))