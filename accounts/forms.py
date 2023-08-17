from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
# from django.contrib.auth.hashers import check_password

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'phone', 
                  'country', 'city', 'language', )

# class CheckPasswordForm(forms.Form):
#     password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
#         attrs={'class': 'form-control',}
#     ))
    
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = self.user.password
        
#         if password:
#             if not check_password(password, confirm_password):
#                 self.add_error('password', '비밀번호가 일치하지 않습니다.')