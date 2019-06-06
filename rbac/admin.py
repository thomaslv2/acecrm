from django.contrib import admin
from rbac import models
class PermissionModelAdmin(admin.ModelAdmin):
    list_display = ['title','url','menu','parent','name']
    list_editable = ['url','menu','parent','name']

class MenuModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'weight']
    list_editable = [ 'weight']
admin.site.register(models.Permission,PermissionModelAdmin)
# admin.site.register(models.User)
admin.site.register(models.Role)
admin.site.register(models.Menu,MenuModelAdmin)
