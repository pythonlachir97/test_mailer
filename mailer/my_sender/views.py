from django.http.response import BadHeaderError, HttpResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail, EmailMultiAlternatives,get_connection
from mailer.settings import EMAIL_HOST_USER
from .forms import ContactForm

def index(request):
    if request.method == "POST":
             
        form = ContactForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                connection = get_connection() # uses SMTP server specified in settings.py
                connection.open() # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()


                from_email = form.cleaned_data['from_email']
                bcc = form.cleaned_data['bcc']
                email_address = form.cleaned_data['email_address']
                cc = form.cleaned_data['cc']
                reply_to = form.cleaned_data['reply_to']
                
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                html_content = form.cleaned_data['html_content']
                attach = request.FILES.getlist('attach')
                email = EmailMultiAlternatives(
                    subject = subject, 
                    body = message,
                    from_email = from_email,
                    to = [email_address],
                    bcc=bcc,
                    cc=cc,
                    reply_to=reply_to,
                    #headers={'MY-UNIQUE-HEAD':  '<http://www.xyz1234.de/unsubscribe123'},
                    connection=connection

                    )
                if html_content:
                    email.attach_alternative(html_content, "text/html")

                if 'attach' in request.FILES:
                    for attachment in attach:
                        email.attach(attachment.name, attachment.read(), attachment.content_type)
                email.send()
                connection.close()

                return HttpResponse('sent')

            except BadHeaderError:
                return render(request, 'my_sender/index.html', {'form':ContactForm(), 'from':EMAIL_HOST_USER, 'message':"something went wrong"})
        else:
            return render(request, 'my_sender/index.html', {'form':ContactForm(), 'message':"Error occured, please try again", 'from':EMAIL_HOST_USER})
    else:
        return render(request, 'my_sender/index.html', {'form':ContactForm(), 'from':EMAIL_HOST_USER})
