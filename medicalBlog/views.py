from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Blog
from users.models import Profile
from .forms import BlogForm 
from .decorators import doctor_access_only, author_access_only

# Create your views here.
@login_required(login_url='login')
def all_blogs(request):
    blogs = Blog.objects.filter(draft=False)
    context = {'blogs':blogs}
    return render(request, 'medicalBlog/blogs.html', context)

@login_required(login_url='login')
def blogs(request):
    profile = request.user.profile
    blogs = Blog.objects.filter(author=profile)
    context = {'blogs':blogs}
    return render(request, 'medicalBlog/blogs.html', context)

@login_required(login_url='login')
@doctor_access_only()
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            profile = Profile.objects.get(user=request.user)
            blog.author = profile
            blog.save()
            return redirect('blogs')
    else:
        form = BlogForm()

    context = {'form': form}
    return render(request, 'medicalBlog/create_blog.html', context)

@login_required(login_url='login')
@doctor_access_only()
@author_access_only()
def updateBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    form = BlogForm(instance=blog)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blogs')

    context = {'form':form}
    return render(request, 'medicalBlog/create_blog.html', context)

@login_required(login_url='login')
@doctor_access_only()
@author_access_only()
def deleteBlog(request, pk):
    blogs = Blog.objects.filter(draft=False)
    blog = Blog.objects.get(id=pk)
    if request.method == "POST":
        blog.delete()
        return redirect('blogs')
    context = {'blog': blog}
    return render(request, 'medicalBlog/delete_confirm.html', context)

def printDetails(request):
    print(request.user.profile.account_user_type)
