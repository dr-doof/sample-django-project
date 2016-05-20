from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm, SignUpForm
from .models import SignUp

# Create your views here.
def home(request):
	title="Sign Up Now"
	#if request.user.is_authenticated():
	#	title= "My Title %s" %(request.user)

	form = SignUpForm(request.POST or None)

	context = {"title": title,
				"form" : form,
	}

	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		context= {
			"title":"Thankyou!!"
		}

	if request.user.is_authenticated() and request.user.is_staff:
		# print(SignUp.objects.all())
		# for instance in SignUp.objects.all():
		# 	print instance.full_name
		queryset=SignUp.objects.all().order_by('-timestamp')
		context={
			"queryset" : queryset
		}
	
	return render(request, "home.html", context)

def contact(request):
	title='Contact Us'
	form= ContactForm(request.POST or None)
	if form.is_valid():
		email=form.cleaned_data.get("email")
		message=form.cleaned_data.get("message")
		full_name=form.cleaned_data.get("full_name")
		
		subject= 'Hello'
		from_email= settings.EMAIL_HOST_USER
		to_email = [email]
		contact_message = "Hi There!!! %s via %s" %(to_email, from_email)

		send_mail(subject,contact_message,from_email,to_email, fail_silently=False)
	context= {
		"form" : form,
		"title" : title,
	}
	return render(request, "forms.html", context)