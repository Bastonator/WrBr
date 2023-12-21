from django import forms
from django.forms import ModelForm
from .models import Product_info, Service_info, Usercreatedpage, Order, location_gambia, Tariffs #, feedback
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#class feedbackForm(forms.ModelForm):
    #class Meta:
        #model = feedback
        #fields = ('name', 'email', 'feedback')
        #exclude = ['user']

        #labels = {
            #'name': '',
            #'email': '',
            #'feedback': '',
        #}

        #widgets = {
            #'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            #'email': forms.EmailField(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            #'feedback': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your experience of the webapp and experince here...'}),
        #}


class TariffsForm(forms.ModelForm):
    class Meta:
        model = Tariffs
        fields = ('name', 'page_owner')
        exclude = ['user']

        labels = {
             'name': '',
             'page_owner': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name the tariff'}),
            'page_owner': forms.Select(attrs={'class': 'form-select', 'placeholder': 'This belongs on which page'}),
        }


class location_gambiaForm(forms.ModelForm):
    class Meta:
        model = location_gambia
        fields = '__all__'
        extra_fields = ['tariff_owner', 'page_owner']
        exclude = ['user']

        def get_field_names(self, declared_fields, info):
            expanded_fields = super(location_gambiaForm, self).get_field_names(declared_fields, info)

            if getattr(self.Meta, 'extra_fields', None):
                return expanded_fields + self.Meta.extra_fields
            else:
                return expanded_fields

        labels = {
            '__all__': '',
            'tariff_owner': '',
            'page_owner': '',
        }

        widgets = {
            '__all__': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'price'}),
            'tariff_owner': forms.Select(attrs={'class': 'form-select', 'placeholder': 'saved to...?'}),
            'page_owner': forms.Select(attrs={'class': 'form-select', 'placeholder': 'This belongs on which page'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'address', 'city', 'message', 'phone_number')

        labels = {
            'first_name': '',
            'last_name': '',
            'address': '',
            'city': '',
            'message': '',
            'phone_number': '',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address and house code'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Which region do live in'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Anything you want to add or tell the sellers about the products you are ordering?'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone number'}),
        }


class PageForm(forms.ModelForm):
    class Meta:
        model = Usercreatedpage
        fields = ('id', 'page_name', 'page_description', 'theme_photo', 'location', 'business_name', 'phone_number')
        exclude = ['user']

        labels = {
            'id': '',
            'page_name': '',
            'page_description': '',
            'theme_photo': '',
            'location': '',
            'business_name': '',
            'phone_number': '',
        }

        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link name. Note: make sure there are no spaces.'}),
            'page_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Store name'}),
            'page_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about this store'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where is the business located'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number.'}),
        }

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

        self.fields['theme_photo'].widget = forms.FileInput(
            attrs={'class': 'form-control', 'placeholder': 'Put image here'})


class Product_infoForm(forms.ModelForm):
    class Meta:
        model = Product_info
        fields = ('product_name', 'product_price', 'stock_available', 'image_url', 'image_url2', 'image_url3', 'image_url4', 'page_owner', 'product_description')
        exclude = ['user']

        labels = {
            'product_name': '',
            'product_price': '',
            'stock_available': '',
            'image_url': '',
            'image_url2': '',
            'image_url3': '',
            'image_url4': '',
            'product_description': '',
            'page_owner': '',
        }

        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'},),
            'product_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'stock_available': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'How much available?'}),
            'page_owner': forms.Select(attrs={'class': 'form-select', 'placeholder': 'This belongs on which page'}),
            'product_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }

    def __init__(self, *args, **kwargs):
        super(Product_infoForm, self).__init__(*args, **kwargs)

        self.fields['image_url'].widget = forms.FileInput(
            attrs={'class': 'form-control', 'placeholder': 'Put image here'})
        self.fields['image_url2'].widget = forms.FileInput(
            attrs={'class': 'form-control', 'placeholder': 'Put image here'})
        self.fields['image_url3'].widget = forms.FileInput(
            attrs={'class': 'form-control', 'placeholder': 'Put image here'})
        self.fields['image_url4'].widget = forms.FileInput(
            attrs={'class': 'form-control', 'placeholder': 'Put image here'})


class Service_infoForm(ModelForm):
    class Meta:
        model = Service_info
        fields = ('service_name', 'service_price', 'location', 'image_url', 'page_owner')
        exclude = ['user']

        labels = {
            'service_name': '',
            'service_price': '',
            'location': '',
            'image_url ': '',
            'page_owner': '',
        }

        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'what is the service name'}),
            'service_price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'how much is it'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'where is it'}),
            'page_owner': forms.Select(attrs={'class': 'form-select', 'placeholder': 'THIS BELONGS ON WHICH PAGE'}),
        }


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'phone_number')


    def __init__(self, *args, **kwargs):
        super(SignupForm, self). __init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Password Confirmation'
        self.fields['password2'].label = ''




