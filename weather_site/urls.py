from django.urls import path, re_path,register_converter
from . import views
from django.conf.urls.static import static
from django.conf import settings
from . import converters
register_converter(converters.DateConverter, 'yyyy_mm_dd')
urlpatterns = [
    path('<yyyy_mm_dd:date>/', views.MainPage.as_view(), name='forecast'),
    path('', views.MainPage.as_view(), name='forecast'),
    path('archive/', views.ArchivePage.as_view(), name='archive'),
    path('signup/',views.SignupPage.as_view(),name='signup'),
    path('login/',views.LoginPage.as_view(),name='login'),
    path('logout/', views.LogoutPage.as_view(), name='logout'),
    path('account/', views.AccountPage.as_view(), name='account'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)