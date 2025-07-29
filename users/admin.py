from django.contrib import admin
from users.models import UserContactModel,PasswordResetOtp

admin.site.register(UserContactModel)
admin.site.register(PasswordResetOtp)
