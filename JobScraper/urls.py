from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrapByTerm',views.scrapByTerm, name="scrapByTerm"),
    path('create_account',views.create_account, name="create_account" ),
    path('loginPage',views.loginPage, name="loginPage"),
    path('logoutPage',views.logoutPage, name="logoutPage"),
    path('authentication',views.authentication, name="authentication"),
    path('saveListing',views.saveListing, name="saveListing"),
    path('addToHistory',views.addToHistory, name="addToHistory"),
    path('savedListings',views.savedListings, name="savedListings"),
    path('history',views.history, name="history"),
    path('saveCustomListing',views.saveCustomListing, name="saveCustomListing"),
    path('customList/<str:listName>',views.customList, name="customList"),
    path('lists',views.lists, name="lists"),
    path('createList',views.createList, name="createList")
]
