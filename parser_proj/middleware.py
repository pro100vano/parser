import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.deprecation import MiddlewareMixin

from notifications_app.repositories import NotificationRepository


class LoginRequiredMiddleware(MiddlewareMixin):

    @staticmethod
    def is_public_url(url):
        public_view_urls = getattr(settings, 'PUBLIC_URLS', ())
        public_view_urls = [re.compile(v) for v in public_view_urls]
        return any(public_url.match(url) for public_url in public_view_urls)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            notif_rep = NotificationRepository(request.user)
            request.notifications = notif_rep.get_some(5)
            request.notifications_count = notif_rep.get_unread_count()
            return None
        elif self.is_public_url(request.path_info):
            return None

        return login_required(view_func, login_url=reverse_lazy('auth'))(request, *view_args, **view_kwargs)
