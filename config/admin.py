from django.contrib import admin

from authentication.models import Institution
from config.models import AgencyPricing, InsuranceApiUrlConfig


class InstituionsInline(admin.TabularInline):
    model = Institution
    list_display = ('name',)

@admin.register(AgencyPricing)
class PricingAdmin(admin.ModelAdmin):

    inlines = [
        InstituionsInline,
    ]
    list_editable = ['price']
    exclude = ['added_by']
    list_display = ['added_by','date_added','category','price']

    def save_model(self, request, obj, form, change):
        """ add user to Asset Number Function """
        try:
            obj.added_by.id
        except:
            print('no owner')
            obj.added_by = request.user

        super(PricingAdmin, self).save_model(request, obj, form, change)

@admin.register(InsuranceApiUrlConfig)
class InsuranceApiUrlConfigAdmin(admin.ModelAdmin):

    list_editable = ['api_url']
    exclude = ['added_by']

    list_display = ['added_by', 'date_added', 'api_url', 'key_identifier']

    def save_model(self, request, obj, form, change):
        """ add user to Asset Number Function """
        try:
            obj.added_by.id
        except:
            print('no owner')
            obj.added_by = request.user

        super(InsuranceApiUrlConfigAdmin, self).save_model(request, obj, form, change)