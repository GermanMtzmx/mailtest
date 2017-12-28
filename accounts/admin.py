from django.contrib import admin




class UserAdmin(admin.ModelAdmin):
    """User admin"""

    exclude = ('renewed',)
    list_display = ('username', 'email',
        'isActive', 'created', 'modified')
    list_filter = ('isActive',)

    search_fields = ('firstName',
        'lastName', 'username', 'email')


class SocialTokenAdmin(admin.ModelAdmin):
    """Social token admin"""

    list_display = ('token',
        'social', 'user', 'created')

    search_fields = ('token',)


#admin.site.register(User, UserAdmin)
#admin.site.register(SocialToken, SocialTokenAdmin)
