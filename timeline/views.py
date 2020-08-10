import os
import arrow
from xhtml2pdf import pisa
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse
from .forms import NewAccomplishmentForm
from .models import Accomplishment
from bragsheet_io import settings

class AccomplishmentListView(LoginRequiredMixin, ListView):
    model = Accomplishment
    template_name = 'timeline/timeline.html'
    context_object_name = 'accomplishments'
    ordering = ['-date']
    paginate_by = 10

    def get_queryset(self):
        return Accomplishment.objects.filter(user=User.objects.get(username=self.kwargs['username'])).order_by('-date')

class AccomplishmentDetailView(LoginRequiredMixin, DetailView):
    model = Accomplishment

class CompanyAccomplishmentListView(ListView):
    model = Accomplishment
    template_name = 'timeline/company_accomplishments.html'
    context_object_name = 'accomplishments'
    paginate_by = 10

    def get_queryset(self):
        return Accomplishment.objects.filter(user=User.objects.get(username=self.kwargs['username']), company=self.kwargs.get('company')).order_by('-date')

class JobTitleAccomplishmentListView(ListView):
    model = Accomplishment
    template_name = 'timeline/jobtitle_accomplishments.html'
    context_object_name = 'accomplishments'
    paginate_by = 10 

    def get_queryset(self):
        return Accomplishment.objects.filter(user=User.objects.get(username=self.kwargs['username']), jobTitle=self.kwargs.get('jobtitle')).order_by('-date')

class AccomplishmentCreateView(LoginRequiredMixin, CreateView):
    model = Accomplishment
    form_class = NewAccomplishmentForm
    success_url = '/timeline/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_initial(self, *args, **kwargs):
        initial = super(AccomplishmentCreateView, self).get_initial(**kwargs)
        initial = {'date': timezone.now, 'jobTitle': self.request.user.profile.jobTitle, 'company': self.request.user.profile.company}
        self.success_url += self.request.user.username
        return initial
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['type'] = "new"
        return context

class AccomplishmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Accomplishment
    fields = ['date', 'jobTitle', 'company','text']

    def test_func(self):
        accomplishment = self.get_object()
        return self.request.user == accomplishment.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['type'] = "update"
        return context

class AccomplishmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Accomplishment
    success_url = '/timeline/'

    def test_func(self):
        self.success_url += self.request.user.username
        accomplishment = self.get_object()
        return self.request.user == accomplishment.user

def reports(request):
    if request.method == 'POST':
        fromDate = arrow.get(request.POST.get('fromDate')).datetime
        toDate = arrow.get(request.POST.get('toDate')).shift(days=1).shift(minutes=-1).datetime
        accomps = Accomplishment.objects.filter(user=request.user,jobTitle=request.POST.get('jobTitle'), company=request.POST.get('company'), date__range=[fromDate, toDate]).order_by('-date')
        status, response = render_pdf_view(request.user, request.POST.get('jobTitle'), request.POST.get('company'), request.POST.get('toDate'), request.POST.get('fromDate'), request.POST.get('accentColor'), accomps)
        if status.err:
            messages.error(request, 'There was an error creating your report.')
            return redirect('create-report')
        return response
    today = arrow.get().format('YYYY-MM-DD')
    return render(request, 'timeline/reports.html', context={'today': today})

def render_pdf_view(user, jobTitle, company, toDate, fromDate, accentColor, accomplishments):
    template = get_template('timeline/reports_template_1.html')
    context = {
        'user': user,
        'jobTitle': jobTitle,
        'company': company,
        'toDate': arrow.get(toDate).datetime,
        'fromDate': arrow.get(fromDate).datetime,
        'accomplishments': accomplishments,
        'accentColor': accentColor
    }
    # Create Django response object, specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Dispostion'] = 'attachment; filename="' + toDate + '_' + fromDate + '_Accomplishments' + user.first_name + user.last_name + '.pdf"'
    
    # Get the template and render it
    template = get_template('timeline/reports_template_1.html')
    html = template.render(context)
    
    # Create the pdf
    pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    # Return pisaStatus and the response
    return [pisaStatus, response]

def link_callback(uri, rel):
    '''Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources'''
    # Use short variable names
    sUrl = settings. STATIC_URL    # /static/
    sRoot = settings.STATIC_ROOT   # <project dir>/static
    mUrl = settings.MEDIA_URL      # /static/media
    mRoot = settings.MEDIA_ROOT    # <project dir>/static/media

    # converts URIs to absolute system paths
    if uri.startwith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(mRoot, uri.replace(sUrl, ""))
    else:
        return uri # handle absolute uri

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception('media URI must start with %s or %s' %(sUrl, mUrl))

    return path