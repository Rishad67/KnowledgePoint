from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from .models import Profile,Course,Lesson,Registration,Post,Like,Comment,Reply,Course_request
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from guardian.shortcuts import assign_perm
from guardian.decorators import permission_required
from guardian.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import UserForm , ProfileForm ,CourseForm , LessonForm ,PostForm
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.db.models import Q



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
    Registration.objects.create(current_lesson=current_lesson,student=student,course=course)
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

        return HttpResponseRedirect(reverse('user_detail',args=(profile.pk,)))


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
        user.save()
        Profile.objects.create(user=user)
        profile=Profile.objects.get(user=user)
        assign_perm("home.change_profile", user, profile)

        return HttpResponseRedirect(reverse('login') )

class InstructorCreate(CreateView):
    form_class = UserForm
    template_name = "profile/instructor_form.html"

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home_page') )

        return super(InstructorCreate,self).dispatch(request,*args,**kwargs)
    
    def form_valid(self,form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        permission = Permission.objects.get(name='Can add Course')
        user.save()
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
    course = Course.objects.filter(active=True)
    business = course.filter(catagory='bu')
    it = course.filter(catagory='it')
    photography = course.filter(catagory='pt')
    health = course.filter(catagory='hf')
    android = course.filter(catagory='an')
    ai = course.filter(catagory='ai')
    web = course.filter(catagory='wd') 
    gameing = course.filter(catagory='gm')
    robotics = course.filter(catagory='rb')
    design = course.filter(catagory='ds')
    machine = course.filter(catagory='mc')
    teaching = course.filter(catagory='tc')
    programming = course.filter(catagory='pl')
    others = course.filter(catagory='ot')
    network = course.filter(catagory='nt')

    context={'business':business,'it':it,'network':network,'photography':photography,'health':health,'android':android,'ai':ai,'others':others,'programming':programming,'teaching':teaching,'machine':machine,'design':design,'robotics':robotics,'gameing':gameing,'web':web}
    return render(request,'course/course_list.html',context=context)    

def aboutInstructor(request,pk):
    context={'instructor':User.objects.get(pk=pk)}
    return render(request,'course/about_instructor.html',context=context)

def courseSearch(request):
     # If the form is submitted
    raw_data = request.GET.get('search_box', None)
    search_list = None
    search = False
    if raw_data:
        search_keys = raw_data.split(" ")
        query = Q(title__icontains=search_keys[0]) | Q(keywards__icontains=search_keys[0]) 
        for key in search_keys[1:]:
            query &= Q(title__icontains=key) | Q(keywards__icontains=key) 

        search_list=Course.objects.filter(query,active=True)
        search = True


    else:
        print("you submitted nothing")

    new_list = Course.objects.order_by('last_update').reverse();
    top_list = Course.objects.order_by('rating').reverse();
    context = {'search':search,'search_list':search_list,'new_list':new_list,'top_list':top_list}
    return render(request,'search_result.html',context=context)  

def incRating(request,pk):
    raw_data = request.GET.get('rating_box', None)
    if raw_data: 
        course = Course.objects.get(pk=pk)
        prev = course.rating
        new = float(raw_data)*0.5+prev*0.5
        course.rating = new
        course.save()

    return HttpResponseRedirect(reverse('student_page'))

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


def userForum(request):
    blog = Post.objects.exclude(user=request.user);
    p = blog.filter(post_type='p');
    i = blog.filter(post_type='i');
    s = blog.filter(post_type='s');
    c = blog.filter(post_type='c');
    m = Post.objects.filter(user=request.user) 
    context={'p':p ,'i':i ,'s':s ,'c':c,'m':m} 
    return render(request,'user_forum.html',context=context)

class PostCreate(LoginRequiredMixin,CreateView):
    model=Post
    form_class = PostForm
    template_name = "course/course_form.html"

    def get_object(self): 
        return None

    def form_valid(self,form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        assign_perm('home.change_post', post.user,post)
        return HttpResponseRedirect(reverse('user_forum'))

class PostUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'home.change_post'
    model=Post
    form_class = PostForm
    template_name = "course/course_form.html"

@permission_required('home.change_post', (Post, 'pk', 'pk'))
def deletePost(request,pk):
    Post.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('user_forum'))

def likePost(request,pk):
    post = Post.objects.get(pk=pk)
    prev = Like.objects.filter(post=post,user=request.user)
    if not prev:
        Like.objects.create(user=request.user,post=post)
    return HttpResponseRedirect(reverse('user_forum')) 

def commentPost(request,pk):
    raw_data = request.GET.get('comment_box', None)
    if raw_data:
        post = Post.objects.get(pk=pk)
        description = raw_data 
        comment = Comment.objects.create(user=request.user,post=post,description=description)
        assign_perm('home.change_comment', request.user,comment)

    return HttpResponseRedirect(reverse('user_forum'))

@permission_required('home.change_comment', (Comment, 'pk', 'pk'))
def deleteComment(request,pk):
    Comment.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('user_forum'))



def replyComment(request,pk):
    raw_data = request.GET.get('reply_box', None)
    if raw_data:
        comment = Comment.objects.get(pk=pk)
        description =  raw_data
        reply = Reply.objects.create(user=request.user,comment=comment,description=description)
        assign_perm('home.change_reply', request.user,reply)

    return HttpResponseRedirect(reverse('user_forum'))

@permission_required('home.change_reply', (Reply, 'pk', 'pk'))
def deleteReply(request,pk):
    Reply.objects.get(pk=pk).delete()
    return HttpResponseRedirect(reverse('user_forum'))

def follow(request,pk):
    instructor = User.objects.get(pk=pk)
    instructor.profile.follower.add(request.user)

    return HttpResponseRedirect(reverse('about_instructor', args=(pk,)))


