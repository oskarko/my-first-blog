from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import Post
from .models import Comment
from .models import Profil
from .forms import PostForm
from .forms import CommentForm
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
# los siguientes son necesarios para las subidas de imágenes
from django.core.urlresolvers import reverse
from .models import Document
from .forms import DocumentForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import ContactForm
# para el envío de mails
from django.core.mail import send_mail
# para la paginación
from django.views.generic import ListView
# para la activación de cuenta de usuario mediante link enviado por email
from .forms import RegistrationForm
import hashlib
import random
import datetime
#
from markdownx.utils import markdownify
from .utils import get_query


def search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'text', ])

        found_entries = Post.objects.filter(entry_query).order_by('-published_date')

    return render(request, 'blog/post_searched_list.html', {'query_string': query_string, 'posts': found_entries})
    #return render(request, 'blog/post_draft_list.html', {'posts': found_entries})


class PostListView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'post_list.html'

# modifico la query antes de devolverla
    def get_queryset(self):
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        for post in posts:
            post.text = markdownify(post.text)
        return posts


# se usa la de arriba. Esta no!
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    for post in posts:
        post.text = markdownify(post.text)
    return render(request, 'blog/post_list.html', {'posts': posts})
# MVT - modelo - vista - template/plantilla


def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.text = markdownify(post.text)
        list_documents = {}
         # buscaremos al autor del post y guardaremos su icono (si lo tiene)
        user_post = User.objects.filter(username=post.author.username.lower())
        # en el diccionario. Lo colocaremos en la firma del post.
        document = Document.objects.filter(author=user_post)
        # ahora hacemos lo mismo con los autores de todos los comentarios (si los hay)
        if document:
            list_documents.update({document.first().author.username: document.first().docfile.url})
        comments = Comment.objects.filter(post=post)
        for comment in comments:
            # por cada comentario buscaremos en la BD el autor del mismo
            user = User.objects.filter(username=comment.author.lower())
            # y de ese usuario buscaremos su avatar asociado a su nick
            document = Document.objects.filter(author=user)
            if document:
                list_documents.update({document.first().author.username: document.first().docfile.url})
            # si existe avatar, (puede ser que no), lo añadimos al diccionario.
        return render(request, 'blog/post_detail.html', {'post': post, 'list_documents': list_documents})
        #y devolvemos la vista con el post (y sus comentarios) y el diccionario con los pares Users - avatars


@login_required
def post_new(request):
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                #post.published_date = timezone.now()  # si queremos que se publique al momento, descomentar y no pasará por Drafts
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog.views.post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog.views.post_list')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog.views.post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)


def add_user(request):
    if request.method == "POST":
        # form = UserForm(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            datas = {}
            datas['username'] = form.cleaned_data['username']
            #mUser = form.cleaned_data['username']
            datas['email'] = form.cleaned_data['email']
            datas['password1'] = form.cleaned_data['password1']
            #mPass = form.cleaned_data['password1']
            #We will generate a random activation key
            # my_key = str(random.randint(1, 1000))
            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            usernamesalt = datas['username']
            #if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
            datas['activation_key'] = hashlib.sha1((str(salt)+str(usernamesalt)).encode('utf-8')).hexdigest()
            # datas['email_path'] = "/ActivationEmail.txt"
            datas['email_subject'] = "Activación de tu cuenta en DjangoGirls"

            form.sendEmail(datas)  # Send validation email
            form.save(datas)  # Save the user and his profile
            #User.objects.create_user(**form.cleaned_data)  # creamos el usuario, autenticamos y logueamos.
            #user = authenticate(username=mUser.strip(), password=mPass,)  # autenticamos por la cookie.
            #login(request, user)
            # redirigimos a la pantalla principal
            #return redirect('post_list')
            return render_to_response('blog/check.html')
    else:
        # form = UserForm()
        form = RegistrationForm()

    return render(request, 'blog/add_user.html', {'form': form})


#View called from activation email. Activate user if link didn't expire (48h default), or offer to
#send a second link if the first expired.
def activation(request, key):
    activation_expired = False
    already_active = False
    profil = get_object_or_404(Profil, activation_key=key)
    if profil.user.is_active is False:
        if timezone.now() > profil.key_expires:
            activation_expired = True  # Display : offer to user to have another activation link (a link in template sending to the view new_activation_link)
            id_user = profil.user.id
        else:  # Activation successful
            profil.user.is_active = True
            profil.user.save()
            #  print('%s %s' % (profil.user.username.strip(), profil.password2))
            #my_user = authenticate(username=str('osquiviris20'), password=str('123456'))
            #if my_user is None:
            #    print('falló auth')
            #elif my_user.is_active:
            #    print(my_user)
            #    my_c_user = get_object_or_404(User, username=my_user)
            #    print(my_c_user)
            #    login(request, my_user)
            #else:
            #    print('nah')
            #return redirect('blog.views.view_user_profile', pk=profil.user.id)
            return render_to_response('blog/registered.html')

    #If user is already active, simply display error message
    else:
        already_active = True  # Display : error message
    # return render(request, 'sblog/activation.html')
    return redirect('post_list')


def new_activation_link(request, user_id):
    form = RegistrationForm()
    datas = {}
    user = User.objects.get(id=user_id)
    if user is not None and not user.is_active:
        datas['username'] = user.username
        datas['email'] = user.email
        # datas['email_path'] = "/ResendEmail.txt"
        datas['email_subject'] = "Nuevo link de activación para DjangoGirls"

        usernamesalt = usernamesalt.encode('utf8')
        datas['activation_key'] = hashlib.sha1((str(salt)+str(usernamesalt)).encode('utf-8')).hexdigest()
        # datas['email_path'] = "/ActivationEmail.txt"

        profil = Profil.objects.get(user=user)
        profil.activation_key = datas['activation_key']
        profil.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=2), "%Y-%m-%d %H:%M:%S")
        profil.save()

        form.sendEmail(datas)
        request.session['new_link'] = True  # Display : new link send

    return redirect('post_list')


# no se usa por ahora.
@login_required
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            # redirigimos a la pantalla principal
            return redirect(reverse('blog.views.list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'blog/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


@login_required
def photo_remove(request, pk):
    document = get_object_or_404(Document, pk=pk)
    #eliminamos la foto de la BD
    storage = document.docfile.storage
    path = document.docfile.path
    storage.delete(path)  # delete file from disk
    document.delete()

    return redirect('blog.views.view_user_profile', pk=request.user.pk)


@login_required
def view_user_profile(request, pk):
     # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(author=request.user, docfile=request.FILES['docfile'])
            newdoc.save()
            # redirigimos a la pantalla principal
            # blog.views.view_user_profile -> todo lo que va detrás de "view." en urls.py como segundo parámetro
            return redirect('blog.views.view_user_profile', pk=request.user.pk)
    else:
        form = DocumentForm()  # A empty, unbound form
    # Load documents for the list page
    documents = Document.objects.filter(author=request.user)
    document = documents.first()

    # Render list page with the documents and the form
    return render_to_response(
        'blog/profile.html',
        {'document': document, 'form': form},
        context_instance=RequestContext(request)
    )


@login_required
def delete_user_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    # solo un usuario puede borrar su propio perfil
    if user.id == request.user.id:
        # deslogueamos al usuario primero,
        # buscamos y eliminamos el usuario de la BD
        logout(request)
        user.delete()
        # redirigimos a la pantalla principal del blog
        # llamando al método post_list
    return redirect('blog.views.post_list')


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name', '')
            message = request.POST.get('message', '')
            email = request.POST.get('email', '')
            #print('contacto desde la web %s %s %s' % (name, email, message))
            send_custom_email(name, email, message)
            # redirigimos a la pantalla principal
            #return redirect('post_list')
            return render_to_response('blog/thankyou.html')
    else:
        form = ContactForm()

    return render(request, 'blog/contact.html', {'form': form})


def send_custom_email(name, email, message):
    send_mail('Contact from Django Girls', 'Texto:\n\n%s \n\nuser: %s\nemail: %s' % (message, name, email), email, ['oscar.garrucho@gmail.com'], fail_silently=False)
