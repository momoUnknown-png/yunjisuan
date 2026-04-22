from functools import wraps
from django.shortcuts import redirect, render
from .models import WeChatUser, Status
from config import APP_CODE
from settings import ENVIRONMENT


def auto_register_wechat_user(user):
    """自动注册 WeChatUser 的公共函数"""
    try:
        WeChatUser.objects.get(user=user)
    except WeChatUser.DoesNotExist:
        return WeChatUser.objects.create(
            user=user,
            email=f"{user.username}@example.com",
            motto="欢迎使用朋友圈！",
            region="未知地区",
            pic="buzz.png"
        )
    return None


def auto_register_required(view_func):
    """自动注册装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            auto_register_wechat_user(request.user)
        return view_func(request, *args, **kwargs)
    return wrapper


def home(request):
    return render(request, 'homepage.html')


@auto_register_required
def show_user(request):
    user_id = request.user.id
    wechat_user = WeChatUser.objects.get(user_id=user_id)
    return render(request, 'user.html', {'user': wechat_user})


def show_status(request):
    statuses = Status.objects.all()
    return render(request, 'status.html', {'statuses': statuses})


@auto_register_required
def submit_post(request):
    user = WeChatUser.objects.get(user=request.user)
    text = request.POST.get('text')
    if text:
        status = Status(user=user, text=text)
        status.save()
        if ENVIRONMENT == 'dev':
            return redirect('/status')
        elif ENVIRONMENT == 'stag':
            return redirect(f'/stag--{APP_CODE}/status')
    return render(request, 'my_post.html')