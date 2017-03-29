from django.shortcuts import redirect

from bank.models import Session


class Auth:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        no_redirect_urls = ['/user/login/', '/user/registration/']
        if request.get_full_path() in no_redirect_urls:
            response = self.get_response(request)
            return response
        try:
            user_session = request.COOKIES['user-session']
            session = Session.objects.filter(token=user_session).last()
            request.user = session.user
            if not session:
                return redirect('user:login')
        except KeyError:
            return redirect('user:login')
        response = self.get_response(request)
        return response

