from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    
    path('', views.home, name="home"),
    
    path('user/', views.userPage, name="user-page"),
    path('account/', views.accountSettingsCustomer, name="accountSettingsCustomer"),
    
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('UpdateCustomerInfo/<str:pk>/', views.UpdateCustomerInfo, name="UpdateCustomerInfo"),

    path('CustomerInfoPDF/<pk>/', views.render_pdf_view, name="CustomerInfoPDF"),
    
    path('products/', views.products, name="products"),
    path('create_product/', views.createProduct, name="create_product"),
    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

]
