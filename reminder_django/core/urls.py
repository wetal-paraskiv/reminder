from django.urls import path

from . import views
from . views import (
    RecycleRemindView,
    CreateRemindView,
    UpdateReminderView,
    DeleteReminder,
    SearchRemindView,
)

app_name = 'core'

urlpatterns = [
    path('', views.python, name='python'),
    path('home/', views.home, name='home'),
    path('create/', CreateRemindView.as_view(), name='create'),
    path('update/<int:pk>/', UpdateReminderView.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteReminder.as_view(), name='delete'), # dynamic url path
    path('message/', views.js_django_message, name='message'),
    path('recycle_bin/', RecycleRemindView.as_view(), name='recycle_bin'),
    path('search/', SearchRemindView.as_view(), name='search'),
    path('get_reminders/', views.js_get_active_reminders, name='get_reminders'),
    path('bin_old_reminder/', views.js_bin_old_reminder, name='bin_old_reminder'),
    path('about/', views.about, name='about'),
    path('wetals/', views.wetals, name='wetals'),
]
