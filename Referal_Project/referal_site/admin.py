from django.contrib import admin
from .models import userData
# Register your models here.
@admin.register(userData)
class userDataAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'password', 'referral_code_used', 'referral_code_generated', 'number_of_referred')