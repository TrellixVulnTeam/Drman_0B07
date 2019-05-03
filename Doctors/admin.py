from django.contrib import admin
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from .widgets import ElrteWidget
from .models import  Loc_Category ,Spec_Category,DoctorsPost  ,ClosingRules , DoctorPostAdmin , Loc_CategoryAdmin , Spec_CategoryAdmin , Map , Comments
# from djangoseo.admin import register_seo_admin
from django.contrib import admin
# from .seo import BasicExample


# from .forms import DoctorPostAdmin
from django.forms import ModelForm

from django.forms.models import BaseInlineFormSet

from leaflet.admin import LeafletGeoAdmin

from leaflet.admin import LeafletGeoAdminMixin



# class openinghoursInlineFormset(BaseInlineFormSet):
#     model = OpeningHours
#
#     def __init__(self, *args, **kwargs):
#         super(openinghoursInlineFormset, self).__init__(*args, **kwargs)
#         if self.request.GET.get('something', None):
#             # build your list using self.request
#             self.initial = [{'weekday': 'A',}, {'weekday':'B'} ,{'weekday':'B'},{'weekday':'B'},{'weekday':'B'},{'weekday':'B'},{'weekday':'B'}]
#
#
#

#
#     def get_formset(self , request , obj=None , **kwargs):
#         formset = super(openinghoursModelInline, self).get_formset(request , obj , **kwargs)
#         formset.request = request
#         return  formset
#     def get_extra(self , request , obj = None , **kwargs):
#         extra = super(openinghoursModelInline, self).get_extra(request ,  obj , **kwargs)
#         from_hour = request.GET.get('from_hour' , None)
#         to_hour = request.GET.get('to_hour' ,None)
#         if from_hour:
#              extra = 7
#         if to_hour:
#             extra = 7
#         return extra



# class MyModelAdmin(admin.ModelAdmin):
#         formfield_overrides = {models.TextField: {'widget': AdminMarkItUpWidget}}


# class DoctorsPostAdmin(admin.ModelAdmin) :
#     change_list_template = 'admin/Doctorsposts/doctorspost_cat.html'
#

# class DoctorpostForm(ModelForm) :
#     class Meta:
#         model = DoctorsPost
#         fields = '__all__'
#
#         def __init__(self, *args, **kwargs):
#             super(DoctorpostForm, self).__init__(*args, **kwargs)
#
#             self.fields["category"].widget = CheckboxSelectMultiple()
#             self.fields["category"].queryset = Category.objects.all()


# class DoctorpostAdmin(admin.ModelAdmin):
#
#     # change_form_template = 'doctors/categories.html'
#
#     # form = DoctorForm
#     class Media:
#         js = ('ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
#               'admin/js/mselect-to-mcheckbox.js' ,)
#         css = {
#           'all': ('admin/css/mselect-to-mcheckbox.css', ) ,
#         }
    #
    # def get_osm_info(self):
    #     pass
    #
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['osm_data'] = self.get_osm_info()
    #     return super().change_view(
    #         request, object_id, form_url, extra_context=extra_context,
    #     )

# class CategoryAdmin(DjangoMpttAdmin) :
#     form = DoctorForm
#
# class DoctorPostAdminForm(forms.ModelForm) :
#      category = TreeManyToManyField('Category', verbose_name=_("Categories"), editable=True)
#
#      class Meta(object) :
#          model = DoctorsPost
#
# class DoctorPostAdmin(admin.ModelForm):
#       form = DoctorPostAdminForm

# class PoiLocationInline(LeafletGeoAdminMixin, admin.StackedInline):
#     model = DoctorsPost


# class mapAdmin(LeafletGeoAdmin) :
#
#     change_form_template = 'admin/Doctors/Map/change_form.html'
#
#     # class Media:
#     #         css = {
#     #           'all': ('admin/assets/dist/css/stylehealth.min.css', ) ,
#     #         }

# admin.site.register(Map , LeafletGeoAdmin)
admin.site.register(Loc_Category , Loc_CategoryAdmin)
admin.site.register(Comments)
# admin.site.register(Item , ItemAdmin)
# admin.site.register(WeatherStation, LeafletGeoAdmin)
# admin.site.register(OpeningHours , OpeningHoursAdmin)
admin.site.register(ClosingRules)
admin.site.register(Spec_Category , Spec_CategoryAdmin)
admin.site.register(DoctorsPost , DoctorPostAdmin)
# register_seo_admin(admin.site, BasicExample)
# admin.site.register(weekdays)
# admin.site.site_header = "Administration"
