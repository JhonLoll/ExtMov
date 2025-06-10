from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('extrato/', extrato, name='extrato'),
    path('dashboard/', extrato, name='dashboard'),  # Alias
    path('logout/', sair, name='logout'),
    path('extrato/upload/', upload_extrato, name='upload_extrato'),
]