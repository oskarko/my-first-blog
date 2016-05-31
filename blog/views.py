from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import Post
from .models import Comment
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


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
# MVT - modelo - vista - template/plantilla


def post_detail(request, pk):
        post = get_object_or_404(Post, pk=pk)
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
                post.published_date = timezone.now()
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
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)  # creamos el usuario, autenticamos y logueamos.
            user = authenticate(username=request.POST.get('id_username', '').strip(), password=request.POST.get('id_password', ''),)  # autenticamos por la cookie.
            login(request, user)
            # redirigimos a la pantalla principal
            return redirect('blog.views.post_list')
    else:
        form = UserForm()

    return render(request, 'blog/add_user.html', {'form': form})


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
