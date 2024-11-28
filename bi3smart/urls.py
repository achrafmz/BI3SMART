from django.urls import path
from bi3smart.views import index, detail, shop ,product_list,CategoryDetailView, add_to_cart,home,product_create,contact,contact_list,chat_view,dashboard,user_login,user_register,user_logout,cart,update_quantity,checkout
from . import views
urlpatterns = [
    path('', index, name='home'),
    path('<int:myid>', detail, name="detail"),
    path('shop/',shop , name="shop"),
    path('shop/<int:myid>/', detail, name='detail'),
    path('products/', product_list, name='product_list'),
    path('product/create/', product_create, name='product_create'),
    path('product/<int:pk>/update/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('contact/', contact, name='contacte'),
    path('contact_list/', contact_list, name='contact'),
    path('chat/', chat_view, name='chat'),
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('cart/', cart, name='cart'),
    path('update-quantity/<int:item_id>/', update_quantity, name='update-quantity'),
    path('checkout/', checkout, name='checkout'),
    path('test/', home, name=''),
    path('<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),








  






    
]