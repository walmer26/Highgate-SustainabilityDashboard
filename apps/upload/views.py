from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import ReportForm

class ReportUploadView(LoginRequiredMixin, View):
    def get(self, request):
        form = ReportForm()
        return render(request, 'upload/upload_report.html', {'form': form})

    def post(self, request):
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Report uploaded successfully.')
            except ValidationError as e:
                messages.error(request, e.message)
            return redirect(reverse('upload:upload_report'))
        return render(request, 'upload/upload_report.html', {'form': form})
