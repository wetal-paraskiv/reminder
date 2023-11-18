from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import render, redirect, get_object_or_404

from . models import Reminder
from django.views import generic
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)

from django.urls import reverse_lazy
from . forms import ReminderForm, EditReminderForm
from django.db.models import Q

from django.core.serializers import serialize
from django.http import HttpResponse
import json

        
def js_get_active_reminders(request):
    if request.method == 'GET':
        user = get_object_or_404(User, username=request.user)
        qs = Reminder.objects.filter(
            author=user, active=True)
        data = serialize("json", qs, fields=('text', 'date', 'repeat'))
        return HttpResponse(data, content_type="application/json")


def js_bin_old_reminder(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        reminder_id = data['pk']

        reminder = Reminder.objects.get(id=reminder_id)
        reminder.active = False
        reminder.save()

        return JsonResponse('Reminder was Binned..', safe=False)


def js_django_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        pk = data['pk']

    reminder = get_object_or_404(Reminder, pk=pk)
    messages.success(request, reminder.text)
    return JsonResponse('Ok.. thanks! detail alert view started..', safe=False)


class SearchRemindView(generic.ListView):
    model = Reminder
    template_name = 'core/search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query == None:
            query = ''
        user = get_object_or_404(User, username=self.request.user)
        object_list = Reminder.objects.filter(author=user, active=True).filter(
            Q(text__icontains=query)
        ).order_by('date')
        return object_list


class RecycleRemindView(generic.ListView):

    model = Reminder
    template_name = 'core/recycle_bin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.request.user)

        context["bin_reminders"] = Reminder.objects.filter(
            author=user).filter(active=False).order_by('date')
        return context


class CreateRemindView(LoginRequiredMixin, CreateView):
    model = Reminder
    form_class = ReminderForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy('core:home')


class UpdateReminderView(UpdateView):
    model = Reminder
    form_class = EditReminderForm
    # fields = ['text', 'date', 'active', 'repeat']
    template_name_suffix = '_update_form'  # uneste reminder cu template_name_suffix
    success_url = reverse_lazy('core:home')


class DeleteReminder(DeleteView):
    model = Reminder
    success_url = reverse_lazy('core:recycle_bin')


def python(request):
    template_name = 'core/python.html'
    return render(request, template_name)


def home(request):
    template_name = 'core/home.html'
    context = {}
    return render(request, template_name, context)


def about(request):
    template_name = 'core/about.html'
    return render(request, template_name)


def wetals(request):
    template_name = 'core/wetals.html'
    return render(request, template_name)
