# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
# from .forms import CheckPasswordForm

from django.contrib.auth.models import Group

User = get_user_model()

# 회원가입 그룹 선택
@require_http_methods(['GET', 'POST'])
def signup(request):
    return render(request, 'accounts/signup.html')


# "가이드" 회원가입
@require_http_methods(['GET', 'POST'])
def signup_guide(request):
            
    if request.method == 'GET':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Group = request.user.groups.filter(name='guide') 
            group = Group.objects.get(name='guide')
            user.groups.add(group)
    
            auth_login(request, user)
            return redirect('home')
    
    return render(request, 'accounts/signup_guide.html', {
        'form': form,
    })
    
# "투어리스트" 회원가입
@require_http_methods(['GET', 'POST'])
def signup_tourist(request):
    # if not request.user.groups.filter(name="tourist").exists():
    #     return redirect('home')
    
    if request.method == 'GET':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Group = request.user.groups.filter(name='tourist') 
            group = Group.objects.get(name='tourist')
            user.groups.add(group)
            
            auth_login(request, user)
            return redirect('home')
    
    return render(request, 'accounts/signup_tourist.html', {
        'form': form,
    })

# 로그인
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
    else:              
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(request.GET.get('next') or 'home')
    return render(request, 'accounts/login.html', {
        'form': form,
    })

# 로그아웃
def logout(request):
    auth_logout(request)
    messages.success(request, "로그아웃 되었습니다.")
    return redirect('home')

# 프로필 창
@require_safe
def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    # like_guide = request.user.guides.filter(pk=profile_user.pk).exists()
    
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        # 'like_guide': like_guide,
    })

# 찜하기
@require_POST
@login_required
def wishlist(request, username):  # follow=wishlist, guide = star, tourist = fan
    
    guide = get_object_or_404(User, username=username)  # User = get_user_model() 위에 참조
    tourist = request.user
    
    if guide != tourist:  
    
        # 기존에 찜 한 사람이라면 취소, 아니라면 찜 목록에 추가
        if tourist.guides.filter(pk=guide.pk).exists():
            # 기존에 찜한 적 있으면 취소
            tourist.guides.remove(guide)  
        else:
            # 찜 한 적 없으면 위시리스트에 추가
            tourist.guides.add(guide)  

    return redirect('accounts:profile', guide)  # 가이드(star.pk)의 프로필 페이지로 오기 


# 회원정보 수정
from django.contrib.auth.forms import UserChangeForm

@require_POST
def update(request):
    if request.method=='POST':
        pass
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)

# 비밀번호 변경
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        else:
            form = PasswordChangeForm(request.user)
            
        context = {
            'form': form,
        }
        return render(request, 'accounts/signup.html', context)  #


# 탈퇴하기
@require_POST
def delete(request, username):
    profile_user = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        request.user.delete()
        auth_logout(request)
    return redirect('accounts:login')