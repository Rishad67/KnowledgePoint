from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from .models import Profile,Course,Lesson,Registration
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import assign_perm
from guardian.decorators import permission_required
from guardian.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import UserForm , ProfileForm ,CourseForm , LessonForm
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden



# Create your views here.
#model._meta.get_all_field_names() and model._meta.get_fields()
def homePage(request):
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    courses=Course.objects.all()
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'homePage.html',
        context={'num_visits':num_visits,'courses':courses},
    )

@login_required
def indexPage(request):
    if request.user.has_perm('home.add_course'):
        return render(request,'indexPage.html')
    else:
        return render(request,'studentPage.html')

@login_required
def studentPage(request):
    return render(request,'studentPage.html')

@login_required
def instructorPage(request):
    return render(request,'instructorPage.html')

@login_required
def registerCourse(request,pk):
    course = Course.objects.get(pk=pk)
    current_lesson=course.lesson_set.get(lesson_no=1)
    student=request.user
    Registration.objects.create(student=student,course=course,current_lesson=current_lesson)
    assign_perm('home.view_course_lessons', student, course)
    return HttpResponseRedirect(course.get_absolute_url())

@permission_required('home.change_course', (Course, 'pk', 'pk'))
def launchCourse(request,pk):
    course = Course.objects.get(pk=pk)
    if course.active == False :
        course.active=True
        course.save()
    return HttpResponseRedirect(course.get_absolute_url())


class ProfileUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'home.change_profile'
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
        instructor = form.cleaned_data['instructor']
        user.save()
        if instructor == True :
            permission = Permission.objects.get(name='Can add Course')
            user.user_permissions.add(permission)
            user.save()
        Profile.objects.create(user=user)
        profile=Profile.objects.get(user=user)
        assign_perm("home.change_profile", user, profile)

        return HttpResponseRedirect(reverse('login') )

class UserDetailView(LoginRequiredMixin,generic.DetailView):
    model = Profile
    template_name = 'profile/user_detail.html'


class CourseCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'home.add_course'
    model=Course
    form_class = CourseForm
    template_name = "course/course_form.html"

    def get_object(self): 
        return None

    def form_valid(self,form):
        course = form.save(commit=False)
        if self.request.user.is_authenticated():
            course.instructor = self.request.user
        mycourse=Course.objects.filter(title__exact=course.title,instructor__exact=course.instructor)
        if mycourse:
            return HttpResponseRedirect(reverse('instructor_page') )
        else:
            course.save()
            assign_perm('home.change_course', course.instructor,course)
            return HttpResponseRedirect(course.get_absolute_url())

def courseList(request):
    context={'course_list':Course.objects.filter(active__exact=True)}
    return render(request,'course/course_list.html',context=context)    


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'course/course_detail.html'
    def get_object(self):
        object = super(CourseDetailView, self).get_object()
        self.request.session['course_pk']=object.pk
        return object

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll'] = True
        if self.request.user.is_authenticated():
            registration = context['course'].registration_set.filter(student__exact=self.request.user)
            if registration :
                context['enroll'] = False
                
        return context

class CourseUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'home.change_course'
    model=Course
    form_class = CourseForm
    template_name = "course/course_form.html"


class LessonCreate(PermissionRequiredMixin,CreateView):
    form_class = LessonForm
    template_name = "course/course_form.html"
    permission_required = 'home.change_course'

    def get_object(self): 
        course_pk= self.request.session.get('course_pk')
        course = Course.objects.get(pk=course_pk)

        return course

    def form_valid(self,form):
        lesson = form.save(commit=False)
        course_pk= self.request.session.get('course_pk')
        lesson.course = Course.objects.get(pk=course_pk)
        mylesson=Lesson.objects.filter(topic__exact=lesson.topic,course__exact=lesson.course)
        if mylesson:
            return HttpResponseRedirect(reverse('instructor_page') )
        else:
            lesson.save()
            assign_perm('home.change_lesson', self.request.user,lesson)
            assign_perm('home.view_course_lessons', self.request.user, lesson.course)
            return HttpResponseRedirect(lesson.get_absolute_url())

class LessonUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'home.change_lesson'
    model=Lesson
    form_class = LessonForm
    template_name = "course/course_form.html"

class LessonDetailView(PermissionRequiredMixin,generic.DetailView):
    permission_required = 'home.view_course_lessons'
    model = Lesson
    template_name = 'course/lesson_detail.html'

    def get_permission_object(self):
        return self.get_object().course
