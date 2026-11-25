from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Group, Question, Answer, Poll, PollOption, PollVote

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Educational Role', {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Educational Role', {'fields': ('role',)}),
    )

admin.site.register(Group)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(PollVote)
