from django import forms
from .models import Post
from .models import Comment
from .models import Profil
from django.contrib.auth.models import User
import datetime
from django.core.mail import send_mail


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        # con widgets colocaremos asteriscos como entrada del password
        widgets = {
            'password': forms.PasswordInput(),
        }


class DocumentForm(forms.Form):

    docfile = forms.FileField(
        label='Seleccione un archivo',
        help_text='max. 42 megabytes'
    )


class ContactForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label=(u'name'), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}), label=(u'email'), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': ''}), required=True)


class RegistrationForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'class': 'form-control input-perso'}), max_length=30, min_length=3)
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'placeholder': 'E-mail', 'class': 'form-control input-perso'}), max_length=100, error_messages={'invalid': ("Email invalide.")})
    password1 = forms.CharField(label="", max_length=50, min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control input-perso'}))
    password2 = forms.CharField(label="", max_length=50, min_length=6,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirme password', 'class': 'form-control input-perso'}))

    #recaptcha = ReCaptchaField()

    #Override of clean method for password check
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            self._errors['password2'] = ["Los passwords no coinciden."]

        return self.cleaned_data

    #Override of save method for saving both User and Profil objects
    def save(self, datas):
        u = User.objects.create_user(datas['username'],
                                     datas['email'],
                                     datas['password1'])
        u.is_active = False
        u.save()
        profil = Profil()
        profil.user = u
        profil.password2 = datas['password1']
        profil.activation_key = datas['activation_key']
        profil.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profil.save()
        return u

    #Handling of activation email sending ------>>>!! Warning : Domain name is hardcoded below !!<<<------
    #I am using a text file to write the email (I write my email in the text file with templatetags and then populate it with the method below)
    def sendEmail(self, datas):
        link = "http://localhost:8000/activate/"+datas['activation_key']
        #f = open(MEDIA_ROOT+datas['email_path'], 'r')
        #t = Template(f.read())
        #f.close()
        #message = t.render(c)
        message = link
        #print unicode(message).encode('utf8')
        send_mail(datas['email_subject'], message, 'yourdomain <no-reply@yourdomain.com>', [datas['email']], fail_silently=False)
