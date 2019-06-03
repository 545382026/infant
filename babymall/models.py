from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Classify(models.Model):
    title = models.CharField(max_length=20, verbose_name='大类别')
    def __str__(self):
        return self.title

    class Meta():
        verbose_name = '大分类'
        verbose_name_plural = verbose_name


class Classifys(models.Model):
    title = models.CharField(max_length=20, verbose_name='小类别')
    title_id = models.ForeignKey(Classify, default=None,  null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    class Meta():
        verbose_name = '小分类'
        verbose_name_plural = verbose_name



class Commodity(models.Model):
    img = models.ImageField(upload_to='img', verbose_name='商品图')
    title = models.CharField(max_length=50, verbose_name='标题')
    ciur_pic = models.SmallIntegerField(verbose_name='现价')
    ori_pic = models.SmallIntegerField(verbose_name='活动价', default=None)
    nub = models.IntegerField(default=0, verbose_name='已售数量')
    discount = models.CharField(max_length=20, default=10, verbose_name='打折')
    cla_id = models.ForeignKey(Classifys, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True, verbose_name='上架时间')

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = '商品'
        verbose_name_plural = verbose_name




class Case(models.Model):
    img = models.ImageField(upload_to='img', verbose_name='商品图')
    title = models.CharField(max_length=50, verbose_name='标题')
    data = models.DateTimeField(auto_now_add=True, verbose_name='发表时间')
    detail = models.CharField(max_length=200, verbose_name='内容')

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = '资讯'
        verbose_name_plural = verbose_name


class MyUser(User):
    phone = models.IntegerField(verbose_name='电话')

    def __str__(self):
        return self.username

    class Meta():
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Shop(models.Model):
    img = models.ImageField(upload_to='img', verbose_name='商品图')
    title = models.CharField(max_length=50, verbose_name='标题')
    color = models.CharField(max_length=20, verbose_name='颜色')
    num = models.IntegerField(default=1, verbose_name='购买数量')
    price = models.SmallIntegerField(verbose_name='单价')
    subtotal = models.SmallIntegerField(verbose_name='小计')
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    class Meta():
        verbose_name = '购物车'
        verbose_name_plural = verbose_name




class Color(models.Model):
    color1 = models.CharField(max_length=20, verbose_name='颜色1', default=None)
    color2 = models.CharField(max_length=20, verbose_name='颜色2', default=None)
    color3 = models.CharField(max_length=20, verbose_name='颜色3', default=None)
    color4 = models.CharField(max_length=20, verbose_name='颜色4', default=None)
    com_id = models.ForeignKey(Commodity, verbose_name='商品外键', on_delete=models.CASCADE)

    def __str__(self):
        return self.color1

    class Meta():
        verbose_name = '颜色'
        verbose_name_plural = verbose_name
