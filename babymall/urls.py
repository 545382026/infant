from django.conf.urls import url
from . import views
app_name = 'babymall'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^commodity/$', views.commodity, name='commodity'),
    url(r'^commoditys/(\d+)/$', views.commoditys, name='commoditys'),


    url(r'^buytoday/$', views.buytodau, name='buytoday'),
    url(r'^information/$', views.information, name='information'),
    url(r'^about/$', views.about, name='about'),

    url(r'^login/$', views.login, name='login'),
    url(r'^loginout/$', views.loginout, name='loginout'),

    url(r'^register/$', views.register, name='register'),

    url(r'^shopcart/(\d+)/$', views.shopcart, name='shopcart'),
    url(r'^details/(\d+)/$', views.details, name='details'),
    url(r'^shopcase/(\d+)/$', views.shopcase, name='shopcase'),

    url(r'^deleone/(\d+)$', views.deleone, name='deleone'),
    url(r'^deleall/$', views.deleall, name='deleall'),

    # 验证码路由
    url(r'^verify/$', views.verify, name='verify'),
]