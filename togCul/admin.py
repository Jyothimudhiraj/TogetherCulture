# from django.contrib import admin

# # Register your models here.
# from .models import Member

# class MemberAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'email', 'approved')
#     list_filter = ('approved',)
#     actions = ['approve_members']

#     def approve_members(self, request, queryset):
#         queryset.update(approved=True)
#     approve_members.short_description = "Approve selected members"

# admin.site.register(Member)


# new code below


from django.contrib import admin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from .models import Member

class MemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'approved')
    list_filter = ('approved',)
    actions = ['approve_members']
    change_form_template = 'admin/member/change_form.html'

    def approve_members(self, request, queryset):
        queryset.update(approved=True)
    approve_members.short_description = "Approve selected members"

    def save_model(self, request, obj, form, change):
        if not obj.approved:
            raise ValidationError("You must approve the member before saving.")
        super().save_model(request, obj, form, change)

    def response_change(self, request, obj):
        if "_save" in request.POST:
            return HttpResponseRedirect("/admin/togCul/member/")
        return super().response_change(request, obj)

admin.site.register(Member, MemberAdmin)