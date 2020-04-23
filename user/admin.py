from django.contrib import admin
from .models import Profile, Message, Fill_Out_Sheet
# Register your models here.
admin.site.register(Profile)
admin.site.register(Fill_Out_Sheet)
admin.site.register(Message)

