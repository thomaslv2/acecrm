# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-03 04:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('icon', models.CharField(blank=True, max_length=56, null=True, verbose_name='图标')),
                ('weight', models.IntegerField(default=1, verbose_name='权重')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255, verbose_name='权限')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('name', models.CharField(max_length=56, verbose_name='路由别名')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu', verbose_name='所属菜单')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Permission', verbose_name='父权限')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='角色')),
                ('permissions', models.ManyToManyField(blank=True, to='rbac.Permission')),
            ],
        ),
    ]
