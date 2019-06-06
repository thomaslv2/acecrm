from django.db import models

class Menu(models.Model):
    name=models.CharField(max_length=32,verbose_name='名称')
    icon=models.CharField(max_length=56,verbose_name='图标',blank=True,null=True)
    weight=models.IntegerField(default=1,verbose_name='权重')
    def __str__(self):
        return self.name


class Permission(models.Model):
    url=models.CharField(max_length=255,verbose_name='权限')
    title=models.CharField(max_length=32,verbose_name='标题')
    name=models.CharField(max_length=56,verbose_name='路由别名')
    menu=models.ForeignKey('Menu',blank=True,null=True,verbose_name='所属菜单')
    parent=models.ForeignKey('Permission',blank=True,null=True,verbose_name='父权限')
    def __str__(self):
        return self.title
class Role(models.Model):
    name=models.CharField(max_length=32,verbose_name='角色')
    permissions=models.ManyToManyField('Permission',blank=True)
    def __str__(self):
        return self.name
    
class User(models.Model):
    # name=models.CharField(max_length=32,verbose_name='用户')
    # pwd=models.CharField(max_length=32,verbose_name='密码')
    roles=models.ManyToManyField(Role,blank=True)
    class Meta:
        abstract=True



