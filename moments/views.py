from .models import WeChatUser, Status
from django.shortcuts import redirect, render

from config import APP_CODE
from settings import ENVIRONMENT

def home(request):
    return render(request, 'homepage.html')


def show_user(request):
    # 获取蓝鲸用户id
    user_id = request.user.id
    # 获取 WeChatUser 对象
    wechat_user = WeChatUser.objects.get(user_id=user_id)
    return render(request, 'user.html', {'user': wechat_user})


def show_status(request):
    statuses = Status.objects.all()
    return render(request, 'status.html', {'statuses': statuses})



def submit_post(request):
    user = WeChatUser.objects.get(user=request.user)
    text = request.POST.get('text')
    if text:
        status = Status(user=user, text=text)
        status.save()
        if ENVIRONMENT == 'dev':
            return redirect(f'/status')
        elif ENVIRONMENT == 'stag':
            return redirect(f'/stag--{APP_CODE}/status')
    return render(request, 'my_post.html')