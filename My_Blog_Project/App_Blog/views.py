from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Blog,Likes
from .forms import BlogForm,CommentForm
import uuid ## random id
from django.urls import reverse,reverse_lazy
from django.views.generic import ListView


@login_required
def myblog(request):
    blogs = Blog.objects.filter(author = request.user)
    return render(request,"App_Blog/my_blogs.html",{'blogs':blogs})

@login_required
def CreateBlog(request):
    form = BlogForm()
    created = False
    if request.method == "POST":
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            blog_obj = form.save(commit=False)
            blog_obj.author = request.user
            ## title is needed for creating slug
            title = blog_obj.blog_title
            blog_obj.slug = title.replace(" ","-")+"-"+str(uuid.uuid4())
            blog_obj.save()
            created = True
            return HttpResponseRedirect(reverse("index"))
    return render(request,'App_Blog/create_blog.html',{'form':form,'created':created})

class BlogList(ListView):
    context_object_name = "blogs"
    model = Blog
    template_name = "App_Blog/blog_list.html"


@login_required
def blog_details(request,slug):
    blog = Blog.objects.get(slug=slug)
    comment_form = CommentForm()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.blog = blog 
            comment.save()
            ## with kwargs we add extra parameter
            return HttpResponseRedirect(reverse("App_Blog:blog_details",kwargs={'slug':slug}))
    return render(request,'App_Blog/blog_details.html',{'blog':blog,'comment_form':comment_form})
            


## making a class based generic update blog
## the decoretor login required is as same as login required 
## mixin as a class based view

class UpdateBlog(LoginRequiredMixin,UpdateView):
    model  = Blog
    fields = ('blog_title','blog_content','blog_image')
    template_name = "App_Blog/edit_blog.html"

    ## when success we need to redirect 
    ## to the blog details with parameter
    def get_success_url(self,**kwargs):
        return reverse_lazy('App_Blog:blog_details',kwargs = {'slug':self.object.slug}) 


@login_required
def liked(request,pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    ##check if already liked
    already_liked = Likes.objects.filter(blog=blog,user=user)
    if not already_liked:
        liked_post = Likes(blog=blog,user=user)
        liked_post.save()
        return HttpResponseRedirect(reverse('App_Blog:blog_details',kwargs={'slug':blog.slug}))
    return HttpResponseRedirect(reverse('App_Blog:blog_details',kwargs={'slug':blog.slug}))

@login_required
def unliked(request,pk):
    blog = Blog.objects.get(pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog,user=user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('App_Blog:blog_details',kwargs={'slug':blog.slug}))