from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView, welcome

urlpatterns = [
    path('', welcome, name='welcome'),
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(), name='google-calendar-init'),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='google-calendar-redirect'),
]
