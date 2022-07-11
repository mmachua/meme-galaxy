
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home.forms import HomeForm, HomeCreate, ProfileForm
from home.models import Post, Friend
from .models import Create
from home.forms import ContactForm, PostForm
from login.models import UserProfile
from .models import Friend
from django.urls import reverse_lazy
from django.db.models import Count, F, Value
from django.db.models.functions import Length, Upper
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import (ListView, UpdateView, CreateView, FormView, DeleteView)
from django.core.exceptions import ObjectDoesNotExist
from home.models import Post,  Aboutpage, Newsletter
from home.forms import ContactForm, NewsletterForm
from django.contrib.auth.decorators import login_required





#@login_required
class HomeView(TemplateView):
    template_name = 'home/home.html'    
    #@login_required
    def get(self, request, pk=None):
        form = HomeForm()
        context = {}
        if pk:
            
            posts = Post.objects.all().order_by('-date')
            form = NewsletterForm()
            #views = Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
            users = User.objects.get(pk=pk)#exclude(id=request.user.id)
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
        else:
            #users = User.objects.get(pk=pk)
           # users = request.user
            form = NewsletterForm()
            posts = Post.objects.all().order_by('-date')
            #friend = Friend.objects.filter()
            #friends = friend.users.all()
        #pass
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        index = posts.number -1
        max_index = len(paginator.page_range)
        start_index = index - 5 if index >=5 else 0
        end_index = index + 5 if index <=max_index -5 else max_index
        page_range = paginator.page_range[start_index:end_index]
            

        args = {'form': form, 'posts': posts,
                'page_range': page_range
                
                # 'users': users,
                # 'friends': friends #'views': views
        }
        return render(request, self.template_name, args)

    def post(self, request):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.user = request.user
            newsletter.save()
            title = 'Thanks!!'
            confirm_message = "Thankyou for subscribing to our newsletter, Email received"
            #args = {'title': title, 'confirm_message': confirm_message }
            return redirect('home:home')
            
        args = {'title': title, 'confirm_message': confirm_message }
        return render(request, self.template_name, args)




#postdetail view
class Post_detailView(TemplateView):
    template_name = 'home/detail.html'

    def get(self, request, id, pk=None):

        if pk:
            post = get_object_or_404(Post, id=id, available=True)
        else:
            post = get_object_or_404(Post, id=id, available=True)

        args = {'post':post}

        return render(request, self.template_name, args)


def like_post(request):
    post = get_object_or_404( Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())    

@login_required
def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
        return redirect('home:memelords')
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('home:memelords') 









#class AboutView(TemplateView):
#    template_name = 'home/About.html'  





#contact form views are here
def contact(request):
    form_class = ContactForm(request.POST or None)

    return render(request, 'home/contact.html', {
        'form': form_class,
    })


@method_decorator(login_required, name='dispatch')
class PostFormView(LoginRequiredMixin, CreateView):
    template_name = 'home/post.html'
    model = Post
    form_class = PostForm
    #fields = '__all__'
    success_url = reverse_lazy('login:view_profile')
    #user = User
    
 
    def form_valid(self, form):
        post = form.cleaned_data.get('post')
        image4 = form.cleaned_data.get('image4')
        image1 = form.cleaned_data.get('image1')
        image2 = form.cleaned_data.get('image2')
        image3 = form.cleaned_data.get('image3')
        form.instance.user = self.request.user
        
        return super().form_valid(form)#, context)


 
@method_decorator([login_required], name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, CreateView):
    template_name = 'home/updateprofile.html'
    model = UserProfile
    success_url = reverse_lazy('login:view_profile')
    form_class = ProfileForm


    def get_object(self):
        try:
            #print("hey are you stuck, contact us for help!")
            #pass
            return self.request.user
        except ObjectDoesNotExist:
            print("hey are you stuck, contact us for help!")

    def form_valid(self, form):
        phone = form.cleaned_data.get('phone')
        image = form.cleaned_data.get('image')
        city = form.cleaned_data.get('city')
        description = form.cleaned_data.get('description')
        website = form.cleaned_data.get('website')
        #form.save(instance=user)
        form.instance.user = self.request.user
        #form.save()
        return super().form_valid(form)
       # messages.success(self.request, 'the update was successfull')

        #return redirect('home:home')


class AboutView(TemplateView):
    template_name = 'home/about.html'


    def get(self, request):
        aboutpages = Aboutpage.objects.all()

        args = {
            'aboutpages': aboutpages
        }
        return render(request, self.template_name, args)

@method_decorator([login_required], name='dispatch')
class MemeLordsView(TemplateView):
    template_name = 'home/memelords.html'
    

    def get(self,request):

        try:
            users = get_object_or_404(id=request.user.id)
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
        
        except:
            
            users = User.objects.exclude(id=request.user.id)
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()

        
        
       

        query = request.GET.get('q')
        if query:

            users = User.objects.filter(
            Q(shop_name__icontains=query)#|
#            Q(user__username__icontains=query)|
#            Q(description__icontains=query)|
            #Q(created__icontains=query)
        )


        args = {  'users': users,
          'friend':friend,
          'friends':friends
        }
        return render(request, self.template_name, args)
