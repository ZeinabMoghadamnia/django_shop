from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView, ListView, DetailView
from .models import Product, Category, Like, Comment
from django.http import JsonResponse, HttpResponseRedirect
from .forms import CommentForm
from django.views import View


# Create your views here.

class HomeView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    queryset = Product.objects.prefetch_related('image').order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryListView(ListView):
    model = Category
    template_name = 'products/categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.filter(parent=None).order_by('name')


# views.py

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'products/category_detail.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        subcategories = Category.objects.filter(parent=category)
        if subcategories.exists():
            context['subcategories'] = subcategories
        else:
            context['products'] = Product.objects.filter(category=category)
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    queryset = Product.objects.prefetch_related('image')
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_details.html'
    context_object_name = 'details'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        description_lines = self.object.description.splitlines()
        context['description_lines'] = description_lines
        context['item_images'] = self.object.image.all()
        context['similar_item'] = Product.objects.filter(category=self.object.category)
        context['like_count'] = self.object.likes.count()
        context['user_has_liked'] = Like.objects.filter(user=self.request.user.pk, product=self.object,
                                                        is_liked=True).exists()
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(status='approved')

        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.get_object()
            comment.author = self.request.user
            if 'reply_to' in request.POST:
                parent_comment_id = int(request.POST['reply_to'])
                parent_comment = Comment.objects.get(id=parent_comment_id)
                comment.reply = parent_comment
            comment.save()


        if 'like_action' in request.POST:
            product = self.get_object()
            like, created = Like.objects.get_or_create(user=self.request.user, product=product)
            like.toggle_like()

        return redirect('products:details', slug=self.object.slug)




class ProductLikeView(View):
    def post(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            product = get_object_or_404(Product, pk=kwargs['pk'])
            like, created = Like.objects.get_or_create(user=request.user, product=product)
            like.toggle_like()
            like_count = product.likes.count()
            return JsonResponse({'is_liked': like.is_liked, 'like_count': like_count})


class ProductSearchView(ListView):
    model = Product
    template_name = 'products/search.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(brand__name__icontains=query)
            ).distinct()
        return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context