from django.contrib import admin

# Register your models here.
from common.models import EmailLog

class EmailAdmin(admin.ModelAdmin):

	list_display = ('email', 'name', 'lastName', 'created')


admin.site.register(EmailLog, EmailAdmin)