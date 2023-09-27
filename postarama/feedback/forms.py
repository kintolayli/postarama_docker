from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField(label="Имя", widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    message = forms.CharField(label="Сообщение", widget=forms.Textarea)
