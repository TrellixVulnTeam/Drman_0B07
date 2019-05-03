from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from Doctors.models import Category
from .utils.fields import MultipleChoiceTreeField
from .models import DoctorsPost , Comments , Loc_Category , Spec_Category
from mptt.models import TreeManyToManyField
from django.forms import CheckboxSelectMultiple
from crispy_forms.helper import FormHelper
from leaflet.forms.widgets import LeafletWidget



# from django.forms import


from datetime import time


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)

class CommentsForm(forms.ModelForm) :

    class Meta:
        model = Comments
        fields = ('name', 'email', 'body')



    name = forms.CharField(widget=forms.TextInput(attrs={
            'id': 'inputName4',
            'class': 'form-control padding-15px',
            'placeholder': 'نام',
    }) , label='نام')

    email = forms.EmailField(
            widget=forms.EmailInput(attrs={'id': 'inputEmail4', 'class': 'form-control padding-15px', 'placeholder':'ایمیل'}), label='ایمیل')

    body = forms.CharField(widget=forms.Textarea(attrs={
            'id': 'exampleFormControlTextarea1',
            'class': 'form-control',
            'placeholder': 'ایمیل',
            'rows': "3" ,
            'style':"height: 120px !important;" }),  label='پرسش')


class DependentForm(forms.ModelForm) :
    dcars = {}
    list_cars = []

    selected_country = Loc_Category.objects.filter()

# ToDo : we have one action and multi form with different class and id , how we can use single view with multi form ?


class searchDetail(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'id' : 'ajab' ,
                                                          'class' : 'search-input b1c w-100 margin-top-15px position-relative',
                                                          'style':"padding: 6px;",
                                                          'placeholder':"نام پزشک و یا تخصص خود را وارد کنید..."}))

    def __init__(self, *args, **kwargs):
        super(searchDetail, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'id' : 'ajab',
                                                          'style':"border: 0; color: #000;",
                                                          'placeholder':"نام پزشک خود را وارد کنید..."}))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class FilterSearchForm(forms.Form):

    # car = forms.ChoiceField(widget=forms.Select(attrs={'required id': 'car', 'name': 'car' ,
    #                                                   'class': 'form-control select2-allow-clear padding-right-10px city2',
    #                                                   'style': "color: #9b9b9b;",
    #                                                   }))

    def __init__(self, *args, **kwargs):

        self.specialty = kwargs.pop('specialty')
        self.brand_choices = kwargs.pop('brand_choices')
        self.car_choices = kwargs.pop('car_choices')

        super(FilterSearchForm, self).__init__(*args, **kwargs)

        self.fields['brand'].choices = self.brand_choices

        self.fields['specialty'].widget = forms.HiddenInput(attrs={'id': 'specialty', 'name': 'specialty', })


        self.fields['car'].widget = forms.Select(attrs={'id': 'car', 'name': 'car', 'placeholder' : 'منطقه' ,
                                                                     'class': 'select2-selection select2-selection--single form-control padding-right-10px city2',
                                                                     'style': "color: #9b9b9b;",

                                                                         })

        self.fields['brand'].widget = forms.Select(attrs={'id': 'brand', 'name': 'brand',
                                                                     'class': 'select2-selection select2-selection--single form-control padding-right-10px city1',
                                                                     'style': "color: #9b9b9b;",
                                                                         })

        if 'brand' in self.data:
            try:
                car_choices = []
                brand = self.data.get('brand')
                cars =  Loc_Category.objects.filter(name=brand)
                for car in cars:
                    for child in car.get_children():
                        car_choices.append((child.name, child.name))

                self.fields['car'].choices = car_choices

            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        else:
            self.fields['car'].choices = self.car_choices

    specialty = forms.CharField()
    brand = forms.ChoiceField()
    car = forms.ChoiceField()

    # brand = forms.ChoiceField(choices=self.choices, widget=forms.Select(attrs={'required id': 'brand', 'name': 'brand',
    #                                                                  'class': 'form-control select2-allow-clear padding-right-10px city1',
    #                                                                  'style': "color: #9b9b9b;",
    #                                                                      }))


    # class MainView(TemplateView):
#     template_name = 'sample_forms/index.html'
#
#     def get(self, request, *args, **kwargs):
#         question_form = QuestionForm(self.request.GET or None)
#         answer_form = AnswerForm(self.request.GET or None)
#         context = self.get_context_data(**kwargs)
#         context['answer_form'] = answer_form
#         context['question_form'] = question_form
#         return self.render_to_response(context)

# class openingHoursInlineAdminForm(forms.ModelForm):
#     class meta:
#         model = OpeningHours
#
#     def
    # weekday = forms.CharField()
    # from_hour = forms.TimeField()
    # to_hour = forms.TimeField()



# openingHoursFormSet = inlineformset_factory(openingHoursForm, extra=7)


def str_to_time(s):
    """ Turns strings like '08:30' to time objects """
    return time(*[int(x) for x in s.split(':')])


def time_to_str(t):
    """ Turns time objects to strings like '08:30' """
    return t.strftime('%H:%M')

def time_choices():
    """Return digital time choices every half hour from 00:00 to 23:30."""
    hours = list(range(0, 24))
    times = []
    for h in hours:
        hour = str(h).zfill(2)
        times.append(hour+':00')
        times.append(hour+':30')
    return list(zip(times, times))

TIME_CHOICES = time_choices()


class Slot(forms.Form):
    opens = forms.ChoiceField(choices=TIME_CHOICES)
    shuts = forms.ChoiceField(choices=TIME_CHOICES)


class MapForm(forms.ModelForm):
    class Meta:
        model = DoctorsPost
        fields = ('geom',)
        widgets = {'geom': LeafletWidget()}



    # def __init__(self, *args, **kwargs):
    #     super(MapForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_show_labels = False



# class DoctorForm(forms.ModelForm):
#     categories = MultipleChoiceTreeField(
#         label=_("Categories"),
#         required=False,
#         queryset=Category.objects.all(),
#     )
#     class Meta:
#         model = DoctorsPost
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super(DoctorForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_action = ""
#         self.helper.form_method = "POST"
#         self.helper.layout = layout.Layout(
#             layout.Field("title"),
#             layout.Field(
#                  "categories",
#                  template="doctors/checkbox_select_multiple_tree.html"
#              ),
#             bootstrap.FormActions(
#                 layout.Submit("submit", _("Save")),
#             )
#         )

# class DoctorForm(forms.ModelForm):
#
#     class Meta:
#         model = DoctorsPost
#         fields= '__all__'
#
#     def __init__(self, *args, **kwargs):
#        TreeManyToManyField  = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple)
