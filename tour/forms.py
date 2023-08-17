from django import forms
from .models import Product, Review, Proposal
# from django_countries.widgets import CountrySelectWidget
# from django_countries.fields import CountryField

class ProductForm(forms.ModelForm):
    title = forms.CharField(
        min_length=2,
        max_length=100,
        label = '투어 이름',
        widget=forms.TextInput(attrs={
            'placeholder': '내용을 입력해주세요',
        })
    )
    
    content = forms.CharField(
        min_length=2,
        widget=forms.Textarea(attrs={
            'placeholder': '투어 내용을 설명해주세요',
        }),
        label='투어 내용'
    )
    
    region = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': '지역을 선택해주세요',
        }),
    )
    
    
    class Meta:
        model = Product
        fields = ('title', 'content', 'country', 'region', 'theme', 'max_personned', ) # 'image',


class ReviewForm(forms.ModelForm):
    
    content = forms.CharField(
        max_length=200,
        widget=forms.Textarea(attrs={
            'placeholder': '최대 200자',
        }),
        label='Review'
    )
    
    class Meta:
        model = Review
        fields = ('score', 'content', )
        
        
class DateInput(forms.DateInput):
    input_type = 'date'
     
class ProposalForm(forms.ModelForm):
    comment = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={
            'placeholder': '가이드에게 하고 싶은 말을 적어주세요! ex) 1. 투어 원하는 시간 2. 해보고 싶은 것 3. 인원수'
        }),
        label='Proposal'
    )
    
    class Meta:
        model = Proposal
        widget = {
            'tour_date': DateInput(),
        }
        fields = ('tour_date', 'personned', 'comment', )