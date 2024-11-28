from django.shortcuts import render, redirect, get_object_or_404
from .models import Product , Contact ,Order,OrderItem,Category
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import ProductForm,ContactForm
import google.generativeai as genai
from django.http import JsonResponse
import json
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

def recommend_products(user):
    # Obtenez les produits les plus populaires achetés par d'autres utilisateurs
    popular_products = Product.objects.annotate(num_purchases=Count('userpurchasehistory')).order_by('-num_purchases')[:5]
    return popular_products

def home(request):
    # Obtenez l'utilisateur actuellement connecté
    current_user = request.user

    # Obtenez les produits recommandés pour l'utilisateur actuel
    recommended_products = recommend_products(current_user)

    return render(request, 'bi3smart/test.html', {'recommended_products': recommended_products})


@csrf_exempt
def update_quantity(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity')
            item = OrderItem.objects.get(id=item_id)
            item.quantity = quantity
            item.save()
            return JsonResponse({'success': True})
        except OrderItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def order_item_count(request):
    # Compter le nombre d'OrderItem
    order_item_count = OrderItem.objects.count()
    
    # Passer le nombre d'OrderItem au template
    context = {
        'order_item_count': order_item_count,
    }
    
    # Rendre le template
    return render(request, 'bi3smart/order_item_count.html', context)

def index(request):
    product_object = Product.objects.all()
    categories = Category.objects.all()
    item_name = request.GET.get('search')
    if item_name != '' and item_name is not None:
        product_object = Product.objects.filter(title__icontains=item_name)
        
    order_item_count = OrderItem.objects.count()
    
    # Passer le nombre d'OrderItem au template
    context = {
        'product_object': product_object,
        'order_item_count': order_item_count,
        'categories': categories,  # Ajouter les catégories au contexte
    }
    return render(request, 'bi3smart/index.html', context)


def detail(request, myid):
    product_object = Product.objects.get(id=myid)
    

    return render(request, 'bi3smart/detail.html', {'product': product_object})


def shop(request):
    product_objects = Product.objects.all()
    categories = Category.objects.all()
    order_item_count = OrderItem.objects.count()

    # Obtenir le terme de recherche de l'URL
    item_name = request.GET.get('search')

    # Filtrer les produits en fonction du terme de recherche
    if item_name and item_name.strip():
        product_objects = product_objects.filter(title__icontains=item_name)
        
    paginator = Paginator(product_objects, 4)
    page_number = request.GET.get('page')
    product_object = paginator.get_page(page_number)

    return render(request, 'bi3smart/shop.html', {'product_object': product_object, 'categories': categories, 'order_item_count': order_item_count})
def product_list(request):
    product_object = Product.objects.all()
    item_name = request.GET.get('search')
    if item_name != '' and item_name is not None:
        product_object = Product.objects.filter(title__icontains=item_name)
    return render(request, 'bi3smart/Product.html', {'product_object': product_object})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirection vers la liste des produits après ajout
    else:
        form = ProductForm()
    return render(request, 'bi3smart/product_create.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')  # Rediriger vers la liste des produits après suppression
    return render(request, 'bi3smart/product_confirm_delete.html', {'product': product})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Rediriger vers la liste des produits après modification
    else:
        form = ProductForm(instance=product)
    return render(request, 'bi3smart/product_form.html', {'form': form})




def contact(request):
    order_item_count = OrderItem.objects.count()
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrez les données du formulaire dans la base de données
            return redirect('success')  # Redirigez vers une page de confirmation ou une autre page
    else:
        form = ContactForm()
    return render(request, 'bi3smart/contact.html', {'form': form, 'order_item_count': order_item_count,'categories': categories})

def contact_list(request):
    contact_object = Contact.objects.all()
    
    return render(request, 'bi3smart/contact_list.html', {'contact_object': contact_object})

GOOGLE_API_KEY = 'AIzaSyCRPt18x6p9hZZD7gTYWjUhlAAZnp6HUZE'
genai.configure(api_key=GOOGLE_API_KEY)

def chat_view(request):
    if request.method == 'POST':
        # Obtenez le message de l'utilisateur à partir du formulaire
        user_input = request.POST.get('user_input', '')

        # Utilisez le modèle de génération pour obtenir la réponse du chatbot
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_input)
        bot_response = ''.join([p.text for p in response.candidates[0].content.parts])

        # Renvoyez le message de l'utilisateur et la réponse du chatbot au template
        return render(request, 'bi3smart/chat.html', {'user_input': user_input, 'bot_response': bot_response})

    return render(request, 'bi3smart/chat.html')


def dashboard(request):
    
    return render(request, 'bi3smart/dashboard.html')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Rediriger vers la page d'accueil après la connexion
    else:
        form = AuthenticationForm()
    return render(request, 'bi3smart/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Rediriger vers la page de connexion après l'enregistrement
    else:
        form = UserCreationForm()
    return render(request, 'bi3smart/register.html', {'form': form})


def checkout(request):
    order_item_count = OrderItem.objects.count()
    categories = Category.objects.all()
    items = OrderItem.objects.all()
    
    # Calcul du total de tous les produits
    total = sum(item.get_total for item in items)
    
    context = {
        'items': items,
        'total': total,
        'order_item_count': order_item_count,
        'categories': categories,
        
    }
    return render(request, 'bi3smart/checkout.html', context)

def cart(request):
    items = OrderItem.objects.all()
    
    order_item_count = OrderItem.objects.count()
    categories = Category.objects.all()
    

    
    # Calcul du total de tous les produits
    total = sum(item.get_total for item in items)
    
    context = {
        'items': items,
        'total': total,
        'order_item_count': order_item_count,
        'categories': categories,
        
    }
    return render(request, 'bi3smart/cart.html', context)



def add_to_cart(request, product_id):
    # Récupérer le produit à ajouter au panier
    product = get_object_or_404(Product, id=product_id)

    # Vérifier s'il existe déjà une commande en cours pour l'utilisateur
    order, created = Order.objects.get_or_create(client=request.user.client, complete=False)

    # Créer un nouvel article de commande associé à la commande de l'utilisateur
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    # Si l'article de commande existe déjà, augmentez simplement la quantité
    if not created:
        order_item.quantity += 1
        order_item.save()

    # Rediriger l'utilisateur vers la page appropriée
    return redirect('product_detail', product_id=product_id)

def login_required_alert(request):
    return render(request, 'login_required.html')



class CategoryDetailView(DetailView):
    model = Category
    template_name = 'bi3smart/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['products'] = category.products.all()
        return context
    
