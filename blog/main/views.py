from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Profile, Post, Comment
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from .forms import RegisterForm




def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'main/register_user.html', {'form': form})

class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'
    success_url = reverse_lazy('home')


class BBLoginView(LoginView):
    template_name = 'main/login.html'
    success_url = reverse_lazy('main:home')


def home(request):
    posts_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts_list, 50)  # Показывать 50 постов на странице

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'main/home.html', {'posts': posts})


def profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    return render(request, 'main/profile.html', {'profile': profile})


def edit_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        # Обновите профиль здесь
        pass
    return render(request, 'main/edit_profile.html', {'profile': profile})


def delete_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        profile.delete()
        return redirect('home')
    return render(request, 'main/confirm_delete.html', {'profile': profile})


def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        # Обновите комментарий здесь
        pass
    return render(request, 'main/edit_comment.html', {'comment': comment})


def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('home')
    return render(request, 'main/confirm_delete.html', {'comment': comment})



from .forms import ProfileForm

def edit_profile(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('main:profile', profile_id=profile.id)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'main/edit_profile.html', {'form': form})