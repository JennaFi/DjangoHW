from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path


from users.apps import UsersConfig
from users.views import UserRegisterView, email_verification, UserUpdateProfile

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email_confirm/<str:token>', email_verification, name='email_confirm'),
    path("edit-profile/", UserUpdateProfile.as_view(), name='edit-profile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)