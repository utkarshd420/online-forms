from django.contrib import admin
from online_forms.models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver
import hashlib
# Register your models here.
class ElementsShowInline(admin.StackedInline):
	model=elements_table
	extra=0
	fieldsets = [
		('Add Elements to Form', {'fields': ['title','description','Input','required','priority']}),
       
	]
class form_object_table_admin(admin.ModelAdmin):
	fieldsets = [
		('Form', {'fields': ['form_title','form_description']}),
       
	]
	inlines = [ElementsShowInline]
	list_display = ('form_title','form_description')
	def queryset(self,request):
		qs = super(form_object_table_admin,self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		else:
			user_ = user_table.objects.get(username=request.user.username)
			form_list = form_table.objects.filter(user=user_)
			return qs.filter(form=form_list)
	def save_model(self,request,obj,form,change):
		obj.response_url = hashlib.md5(request.user.username+obj.form_title).hexdigest()
		obj.form_url = hashlib.sha1(request.user.username+obj.form_title).hexdigest()
		if obj.form_id is None:
			user_ = user_table.objects.get(username=request.user.username)
			curr_form = form_table(user = user_ , form_permissions = 1)
			curr_form.save()
			obj.form_id = curr_form.form_id
		obj.save()

admin.site.register(user_table)
admin.site.register(group_table)
admin.site.register(user_info)
admin.site.register(form_object_table,form_object_table_admin)
admin.site.register(form_table)
admin.site.register(input_object_table)
'''@receiver(pre_save,sender=form_object_table)
def create_form_per_user(sender,instance,**kwargs):
#	print instance.form_id
	if instance.form_id is None:
		curr_form = form_table(user = request.user, form_permissions = 1)
		curr_form.save()
		instance.form_id = curr_form.id
	signals.pre_save.disconnect(create_form_per_user,sender=form_object_table)
	instance.save()
	signals.pre_save.connect(create_form_per_user,sender=form_object_table)'''
