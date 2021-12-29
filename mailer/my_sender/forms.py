from django import forms

class ContactForm(forms.Form):
    from_email = forms.EmailField(max_length = 150)
    bcc = forms.EmailField(max_length = 150,required=False)
    cc = forms.EmailField(max_length = 150,required=False)
    reply_to = forms.EmailField(max_length = 150,required=False)
    email_address = forms.EmailField(max_length = 150)
    subject = forms.CharField(widget = forms.Textarea, min_length = 1, max_length = 10000)
    extra_header = forms.CharField(widget = forms.Textarea, min_length = 1, max_length = 10000,required=False)
    
    message = forms.CharField(widget = forms.Textarea, min_length = 1, max_length = 2000)
    html_content = forms.CharField(widget = forms.Textarea, min_length = 1, max_length = 2000,required=False)

    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)