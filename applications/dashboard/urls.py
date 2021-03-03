from django.urls import path

from applications.dashboard import views

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='login'),
    path('facebook/', views.SocialUserLoginAPI.as_view(), name='api-social-auth-register'),
    path('about-page-view/', views.SocialMediaPages.as_view(), name='about-page-view'),
    path('about-page/', views.FetchAboutPage.as_view(), name='about-page'),
    path('update-page/', views.UpdateAboutPage.as_view(), name='update-page'),
]
