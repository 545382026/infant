# Generated by Django 2.2.1 on 2019-05-29 09:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('babymall', '0002_auto_20190529_1526'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodity',
            name='data',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='上架时间'),
            preserve_default=False,
        ),
    ]
