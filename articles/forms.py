from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        widget=forms.TextInput(
            attrs={
                'class': 'mt-2 form-control',
            }
        )
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class': 'mt-2 form-control',
            }
        )
    )
    category = forms.ChoiceField(
        label='종류',
        choices=Article.CATEGORY_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'mt-2 form-select',
            }
        )
    )

    class Meta:
        model = Article
        exclude = ('user', 'like_users',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': '1',
            }
        )
    )

    class Meta:
        model = Comment
        exclude = ('article', 'user',)
