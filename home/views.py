from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Profile
from django.contrib.auth.models import User
from django.views import generic
from .forms import UserForm , ProfileForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden



# Create your views here.
#model._meta.get_all_field_names() and model._meta.get_fields()
def homePage(request):
    """
    View function for home page of site.
    """

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'homePage.html',
        context={'num_visits':num_visits},
    )

def indexPage(request):
    return render(request,'indexPage.html')

class ProfileUpdate(UpdateView):
    model=Profile
    form_class = ProfileForm
    template_name = "profile/profile_form.html"
    def form_valid(self,form):
        profile = form.save(commit=False)
        profile.user.username = form.cleaned_data['username']
        profile.user.first_name = form.cleaned_data['first_name']
        profile.user.last_name = form.cleaned_data['last_name']
        profile.user.email = form.cleaned_data['email']
        profile.user.save()
        profile.save()

        return HttpResponseRedirect(reverse('index_page') )


class UserCreate(CreateView):
    form_class = UserForm
    template_name = "profile/user_form.html"

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home_page') )

        return super(UserCreate,self).dispatch(request,*args,**kwargs)
    
    def form_valid(self,form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        #print("it is the user" +user)
        user.save()
        Profile.objects.create(user=user)

        return HttpResponseRedirect(reverse('home_page') )

class UserDetailView(generic.DetailView):
    model = Profile
    template_name = 'profile/user_detail.html'


