#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT AUTOMATISÉ POUR OCALM
Ce script va créer tous les fichiers nécessaires et corriger toutes les erreurs
"""

import os
import sys


def create_directory(path):
    """Créer un dossier s'il n'existe pas"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✅ Dossier créé: {path}")


def write_file(filepath, content):
    """Écrire un fichier"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Fichier créé: {filepath}")


def main():
    print("=" * 60)
    print("🚀 INSTALLATION AUTOMATISÉE D'OCALM")
    print("=" * 60)

    # ==================== CRÉATION DES DOSSIERS ====================
    print("\n📁 Création des dossiers...")
    create_directory("pages/templates/pages")
    create_directory("listings/migrations")
    create_directory("escrow/migrations")
    create_directory("wallet/migrations")
    create_directory("accounts/migrations")
    create_directory("templates")
    create_directory("static")
    create_directory("media/listings")

    # ==================== FICHIER settings.py ====================
    print("\n📝 Création des fichiers de configuration...")

    settings_content = '''from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-ocalm-2024-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pages',
    'listings',
    'escrow',
    'wallet',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ocalm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ocalm.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Dakar'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'accounts.User'
'''
    write_file("ocalm/settings.py", settings_content)

    # ==================== FICHIER urls.py ====================
    urls_content = '''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
    write_file("ocalm/urls.py", urls_content)

    # ==================== MODÈLE ACCOUNTS ====================
    accounts_model = '''from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Acheteur'),
        ('seller', 'Vendeur'),
        ('delivery', 'Livreur'),
    )
    phone_number = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
'''
    write_file("accounts/models.py", accounts_model)

    # ==================== MODÈLE LISTINGS ====================
    listings_model = '''import uuid
from django.db import models

class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_name = models.CharField(max_length=150)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=0)
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    image = models.ImageField(upload_to='listings/', blank=True, null=True)
    stock_quantity = models.IntegerField(default=1)
    is_available = models.BooleanField(default=True)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.price} FCFA"
'''
    write_file("listings/models.py", listings_model)

    # ==================== MODÈLE ESCROW ====================
    escrow_model = '''import uuid
from django.db import models

class EscrowTransaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('paid', 'Payé'),
        ('shipping', 'Expédié'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=50, unique=True, editable=False)
    buyer_name = models.CharField(max_length=150)
    seller_name = models.CharField(max_length=150)
    listing_id = models.CharField(max_length=100)
    listing_title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    fee = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=0)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    delivery_otp = models.CharField(max_length=6, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            import random
            self.reference = f"TR{random.randint(10000000, 99999999)}"
        if not self.delivery_otp:
            import random
            self.delivery_otp = str(random.randint(100000, 999999))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} - {self.listing_title}"
'''
    write_file("escrow/models.py", escrow_model)

    # ==================== MODÈLE WALLET ====================
    wallet_model = '''from django.db import models

class Wallet(models.Model):
    user_name = models.CharField(max_length=150, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_name}: {self.balance} FCFA"
'''
    write_file("wallet/models.py", wallet_model)

    # ==================== FICHIER pages/urls.py ====================
    pages_urls = '''from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('listings/', views.listings_view, name='listings'),
    path('listing/create/', views.create_listing_view, name='create_listing'),
    path('listing/<str:listing_id>/', views.listing_detail_view, name='listing_detail'),
    path('listing/<str:listing_id>/edit/', views.edit_listing_view, name='edit_listing'),
    path('listing/<str:listing_id>/delete/', views.delete_listing_view, name='delete_listing'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('withdraw/', views.withdraw_request, name='withdraw'),
]
'''
    write_file("pages/urls.py", pages_urls)

    print("\n" + "=" * 60)
    print("✅ TOUS LES FICHIERS ONT ÉTÉ CRÉÉS AVEC SUCCÈS !")
    print("=" * 60)
    print("\n📋 COMMANDES À EXÉCUTER MAINTENANT :")
    print("-" * 40)
    print("python manage.py makemigrations")
    print("python manage.py migrate")
    print("python manage.py createsuperuser")
    print("python manage.py runserver")
    print("-" * 40)


if __name__ == "__main__":
    main()