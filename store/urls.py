from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required


urlpatterns = [
	path('store/', views.store, name="store"),
	path('cart/', login_required(views.cart), name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	
    path('farmer_profile/', views.farmer_profile, name='farmer-profile'),
    path('add_product/', views.add_product, name='add_product'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path("product_view/<int:myid>/", views.product_view, name="product_view"),
    path('', views.Login, name='login'),
    
    path('logout', login_required(views.logout), name='logout'),
    # path('logout/', login_required(auth.LogoutView.as_view(template_name='store/store.html')), name='logout'),
    path('register/', views.register, name='register'),
    
]