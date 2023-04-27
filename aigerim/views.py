from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from rest_framework import generics, mixins
from django.shortcuts import render
# from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .forms import *
from .models import Aigerim, Category
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import AigerimSerializer

from .utils import *


class AigerimAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000

class AigerimAPIList(generics.ListCreateAPIView):
    queryset = Aigerim.objects.all()
    serializer_class = AigerimSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = AigerimAPIListPagination

class AigerimAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Aigerim.objects.all()
    serializer_class = AigerimSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    # authentication_classes = (TokenAuthentication)

class AigerimAPIDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Aigerim.objects.all()
    serializer_class = AigerimSerializer
    permission_classes = (IsAdminOrReadOnly,)


#ViewSet and ModelViewSet and Router
# class AigerimViewSet(mixins.CreateModelMixin,
#                      mixins.RetrieveModelMixin,
#                      mixins.UpdateModelMixin,
#                      mixins.ListModelMixin,
#                      GenericViewSet):
#     # queryset = Aigerim.objects.all()
#     serializer_class = AigerimSerializer
#
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#
#         if not pk:
#             return Aigerim.objects.all()[:3]
#
#         return Aigerim.objects.filter(pk=pk)
#
#     @action(methods=['get'], detail=True)
#     def category(self, request, pk=None):
#         cats = Category.objects.get(pk=pk)
#         return Response({'cats': cats.name})



class AigerimHome(DataMixin, ListView):
    model = Aigerim
    template_name = 'aigerim/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Aigerim.objects.filter(is_published=True).select_related('cat')

class AigerimCategory(DataMixin, ListView):
    model = Aigerim
    template_name = 'aigerim/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Aigerim.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

class ShowPost(DataMixin, DetailView):
    model = Aigerim
    template_name = 'aigerim/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'aigerim/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    # login_url = '/admin/'
    # raise_exception = True

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить")
        return dict(list(context.items()) + list(c_def.items()))



class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'aigerim/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'aigerim/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')


def about(request):
    contact_list = Aigerim.objects.all()
    paginator = Paginator(contact_list, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'aigerim/about.html', {'page_obj': page_obj, 'menu': menu, 'title': "our_about"})

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'aigerim/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

def bad_request(request, exception=None):
    return render(request, 'content/400.html')
def permission_denied(request, exception=None):
    return render(request, 'content/403.html', {})
def page_not_found(request, exception=None):
    return render(request, 'content/404.html', {})
def server_error(request,exception=None):
    return render(request, 'content/500.html', {})



# class AigerimAPIView(APIView):
#     def get(self, request):
#         a = Aigerim.objects.all()
#         return Response({'posts': AigerimSerializer(a, many=True).data})
#
#     def post(self, request):
#         serializer = AigerimSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = Aigerim.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#
#         serializer = AigerimSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})



# def contact(request):
#     return HttpResponse("Обратная связь")

# def login(request):
#     return HttpResponse("Авторизация")


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

# class AigerimAPIList(generics.ListCreateAPIView):
#     queryset = Aigerim.objects.all()
#     serializer_class = AigerimSerializer
#
# class AigerimAPIUpdate(generics.UpdateAPIView):
#     queryset = Aigerim.objects.all()
#     serializer_class = AigerimSerializer
#
# class AigerimAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Aigerim.objects.all()
#     serializer_class = AigerimSerializer