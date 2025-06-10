from django.db import models

# Importa as bibliotecas para alterar o login
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Modelos para criação do WebApp

# Classe do Usuário
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    def __str__(self):
        return self.email

# Classe do Extrato
class ExtratoMovimentacao(models.Model):
    loja = models.CharField(max_length=100)
    movimentacao = models.CharField(max_length=50)
    local = models.CharField(max_length=100)
    data_lancamento = models.DateField()
    data_movimento = models.DateField()
    codigo_produto = models.IntegerField()
    descricao_produto = models.CharField(max_length=200)
    saldo_anterior = models.DecimalField(max_digits=10, decimal_places=2)
    qtd_movimentada = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_atual = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'extrato_movimentacao'
        verbose_name = 'Extrato de Movimentação'
        verbose_name_plural = 'Extratos de Movimentação'
    
    def __str__(self):
        return f"{self.codigo_produto} - {self.descricao_produto}"