from django import forms




class AccountRegisterForm(forms.Form):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    

    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    gender = forms.ChoiceField(label='Gender', widget=forms.RadioSelect, choices=GENDER_CHOICES)