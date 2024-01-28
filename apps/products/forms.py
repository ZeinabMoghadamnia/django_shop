from ..accounts.models import User
from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['context']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        # می‌توانید اینجا تنظیمات خاصی اضافه کنید، مثلاً افزودن ویژگی‌های ورودی اضافی

    def clean_context(self):
        # اگر نیاز به اعتبارسنجی ویژگی خاصی دارید، می‌توانید آن را اینجا انجام دهید
        context = self.cleaned_data.get('context')
        # اعتبارسنجی مثالی
        if len(context) < 5:
            raise forms.ValidationError("متن کامنت باید حداقل 5 کاراکتر باشد.")
        return context
