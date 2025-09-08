from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BlogPost, UserProfile, BlogImage, Comment

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'contact_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the password help text
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        # Add validation message for contact number
        self.fields['contact_number'].widget.attrs.update({
            'pattern': '[0-9]{10}',
            'title': 'Phone number must be exactly 10 digits'
        })

    def clean_contact_number(self):
        contact_number = self.cleaned_data.get('contact_number')
        if not contact_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")
        if len(contact_number) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits")
        return contact_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Save additional fields in UserProfile
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'contact_number': self.cleaned_data['contact_number']
                }
            )
        return user

class BlogPostForm(forms.ModelForm):
    images = MultipleFileField(required=False)
    image_captions = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text='Enter captions for images, one per line'
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'image', 'images', 'image_captions']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'rich-text-editor'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'custom-textarea',
                'placeholder': 'Tell us about yourself...',
                'style': 'resize: vertical; min-height: 120px;',
            }),
            'website': forms.URLInput(attrs={
                'placeholder': 'https://',
                'class': 'custom-textarea',
                'style': 'min-height: 45px;'
            })
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment...',
                'class': 'comment-input'
            })
        }