from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from PIL import Image, ImageDraw, ImageFont
import random, io
from django.contrib.auth import authenticate, login as lgi, logout as lgo
from django.contrib import messages
# 分页
from django.core.paginator import Paginator
# 缓存
from django.views.decorators.cache import cache_page
from django.core.cache import cache
# Create your views here.
# 提示框


def index(request):
    com = Classify.objects.all()
    com1 = Commodity.objects.all()[:4]
    com2 = Commodity.objects.all()[4:9]
    return render(request, 'index.html', locals())


def commodity(request):

    pagenum = request.GET.get('page')
    pagenum = 1 if pagenum == None else pagenum

    coms = Commodity.objects.all()
    cla = Classify.objects.all()

    num = coms.count()

    # 每一页包含多少条信息
    paginator = Paginator(coms, 6)

    # 传入页码得到一个页面 page包含所有信息
    page = paginator.get_page(pagenum)
    com = page.object_list
    return render(request, 'commodity.html', locals())


def commoditys(request, aid):
    pagenum = request.GET.get('page')
    pagenum = 1 if pagenum==None else pagenum

    cla = Classify.objects.all()
    a = Classifys.objects.get(pk=aid)
    coms = a.commodity_set.all()
    num = coms.count()
    # 每一页包含多少条信息
    paginator = Paginator(coms, 6)

    # 传入页码得到一个页面 page包含所有信息
    page = paginator.get_page(pagenum)
    com = page.object_list
    return render(request, 'commodity.html', locals())

def buytodau(request):
    com = Commodity.objects.all()[6:11]
    print(com)
    return render(request, 'buytoday.html', locals())


def information(request):
    case = Case.objects.all()
    return render(request, 'information.html', locals())


def about(request):
    return render(request, 'about.html')


def login(request):
    """登录"""
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        verifycode = request.POST["verify"]
        print('*********', username, pwd, verifycode)

        print("@@@@@@@@@@@@@@")

        # user = get_object_or_404(MyUser, username=username)
        #
        # check = user.check_password(pwd)
        # 使用中间件，系统自带登录判断
        user = authenticate(request, username=username, password=pwd)
        # print('##########', user, check)
        print(user)
        # 判断账号输入正确
        if user:
            # 判断验证码是否输入正确
            if verifycode == request.session["verifycode"]:
                lgi(request, user)
                return redirect(reverse('babymall:index'))
            else:
                messages.error(request, "验证码错误，请重新输入")
                return render(request, 'login.html')
        else:
            messages.error(request, "账号或密码错误，请重新登录")
            return render(request, 'login.html')


def loginout(request):
    """登出"""
    lgo(request)
    return redirect(reverse('babymall:login'))


def register(request):
    """注册"""
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        pwd1 = request.POST.get('password')
        pwd2 = request.POST.get('password2')
        print(username, pwd1, pwd2)
        # return HttpResponse('你好')

        if MyUser.objects.filter(username=username):
            messages.error(request, "用户已存在，请重新注册")
            return render(request, 'login.html')
        else:
            if pwd1 != pwd2:

                messages.error(request, "两次密码输入不一致，请重新输入")
                return render(request, 'login.html')
            else:
                MyUser.objects.create_user(username=username, password=pwd1, phone=123456)
                messages.success(request, "注册成功，请登录")
                return redirect(reverse('babymall:login'))


def verify(request):
    """
    验证码
    """
    bgcolor = (random.randrange(20, 100),
               random.randrange(20, 100),
               random.randrange(20, 100))
    width = 100
    heigth = 35

    # 创建画面对象
    im = Image.new('RGB', (width, heigth), bgcolor)

    # 创建画笔对象
    draw = ImageDraw.Draw(im)

    # 调用画笔的point()函数绘制噪点
    for i in range(0, 120):
        # 随机取得位置
        xy = (random.randrange(0, width), random.randrange(0, heigth))

        # 随机取得颜色
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))

        # 填充
        draw.point(xy, fill=fill)

    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'

    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

    # 构造字体对象
    font = ImageFont.truetype('FZSTK.TTF', 23)  # 字体需要根据自己电脑上存在的字体设置
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))

    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)

    # 释放画笔
    del draw
    request.session['verifycode'] = rand_str
    f = io.BytesIO()
    im.save(f, 'png')

    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(f.getvalue(), 'image/png')


def shopcase(request, sid):
    """往购物车存储数据， 并重定向到购物车界面"""
    if request.user.username:
        com = Commodity.objects.get(pk=sid)
        user = MyUser.objects.get(username=request.user.username)
        num = request.POST.get('num')
        shop = Shop()
        shop.title = com.title
        shop.img = com.img
        shop.price = com.ciur_pic
        shop.color = '红色'
        shop.num = num
        shop.subtotal = int(com.ciur_pic) * int(num)
        shop.user_id = user
        shop.save()
        return redirect(reverse('babymall:shopcart', args=[user.id, ]))
    else:
        messages.success(request, "账号未登录，请登录")
        return redirect(reverse('babymall:details', args=[sid, ]))


def shopcart(request, sid):
    """购物车界面"""
    print('**********', sid)
    user = MyUser.objects.get(pk=sid)
    return render(request, 'shopcart.html', locals())


def deleone(request, aid):
    """删除单个商品"""
    Shop.objects.get(pk=aid).delete()
    return redirect(reverse('babymall:shopcart'))


def deleall(request):
    """删除所有商品"""
    Shop.objects.all().delete()
    return redirect(reverse('babymall:shopcart'))


def details(request, aid):
    """商品详情界面"""
    com = Commodity.objects.get(pk=aid)
    a = 1
    return render(request, 'details.html', locals())

