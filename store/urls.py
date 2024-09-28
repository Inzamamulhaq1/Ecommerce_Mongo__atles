from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(views.product_list), name='product_list'),
    path('product/<int:pk>/', login_required(views.product_detail), name='product_detail'),
    path('add-to-cart/<int:pk>/', login_required(views.add_to_cart), name='add_to_cart'),
    path('cart/', login_required(views.cart_view), name='cart_view'),
    path('order-summary/', login_required(views.order_summary), name='order_summary'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/', views.logoutView.as_view(),name='logout'),
    path('orders/', login_required(views.order_list), name='order_list'), 
    path('order/<int:pk>/', login_required(views.singleOrder), name='order'), 
    path('register/',views.registerView.as_view(),name='register'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    
    
    
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


