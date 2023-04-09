from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView


from .forms import *
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

class AigerimHome(ListView):
    model = Aigerim
    template_name = 'aigerim/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Aigerim.objects.filter(is_published=True)

class AigerimCategory(ListView):
    model = Aigerim
    template_name = 'aigerim/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Aigerim.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context

class ShowPost(DetailView):
    model = Aigerim
    template_name = 'aigerim/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'aigerim/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить'
        context['menu'] = menu
        return context

def about(request):
    return render(request, 'aigerim/about.html', {'menu': menu, 'title': 'О сайте'})

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'aigerim/addpage.html', {'form': form, 'menu': menu, 'title': "Добавить"})


# def show_post(request, post_slug):
#     post = get_object_or_404(Aigerim, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request,'aigerim/post.html', context=context)

# def show_category(request, cat_id):
#     posts = Aigerim.objects.filter(cat_id=cat_id)
#     cats = Category.objects.all()
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_seletced': cat_id,
#     }
#
#     return render(request, 'aigerim/index.html', context=context)


# def index(request):
#     posts = Aigerim.objects.all()
#     cats = Category.objects.all()
#     context = {
#         'posts': posts,
#         'cats': cats,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'aigerim/index.html', context=context)