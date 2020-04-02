"""pnp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from adventure import views
from django.views.decorators.csrf import csrf_exempt # This is for dev purposes - testing with insomnia
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))), #  This is for dev purposes - testing with insomnia
    # path('graphql/', GraphQLView.as_view(graphiql=True)), # This is for production
    path('test/', views.test, name='map-test'),
    path('', views.home, name='homepage'),
    # path('walking/', views.walksim, name='walking'),
    path('pct/', views.pct, name='playercreationtest')
]
