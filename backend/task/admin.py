from django.contrib import admin
from .models import Task, Tag

class TagAdmin(admin.ModelAdmin):
	list_display = ["pkid", "id", "name", "created"]
	list_filter = ["name"]
	list_display_links= ['id', 'pkid']


class TaskAdmin(admin.ModelAdmin):
	list_display = ["pkid", "id", "user", "title", "income", "expected_pay_day", "actual_pay_day", "submit_day", "client", "agency", "status", "visible", "created"]
	list_filter = ["client", "agency", "status"]
	list_display_links= ['id', 'pkid']


admin.site.register(Tag, TagAdmin)
admin.site.register(Task, TaskAdmin)
