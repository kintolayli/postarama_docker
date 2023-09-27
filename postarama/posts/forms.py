from django import forms
from posts.models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "group",
            "text",
            "tags",
            "status",
            "image",
        ]
        labels = {
            "title": "Заголовок",
            "group": "Группа",
            "text": "Текст",
            "image": "Изображение",
            "tags": "Теги",
            "status": "Статус",
        }

    def clean_body(self):
        data = self.cleaned_data["text"]

        if len(data) < 5:
            raise forms.ValidationError("Пост не может быть длинной меньше 5 знаков.")

        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {
            "text": "Текст",
        }

        widgets = {
            "text": forms.Textarea(attrs={"rows": 3}),
        }


class SearchForm(forms.Form):
    query = forms.CharField()
