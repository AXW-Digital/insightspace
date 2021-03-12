from django.conf.urls import include, url
from django.urls import path, include
from rest_framework import routers
from .views import  (UserAPI, RegistrationAPI, LoginAPI, ChangePasswordAPI, AsiointiViewset, RuokalistaViewset, RavinVaikutuViewset, PerustiedotViewset)
from knox.views import LoginView, LogoutView


router = routers.DefaultRouter()
router.register('asiointi', AsiointiViewset, 'asiointi')
router.register('ruokalista', RuokalistaViewset, 'ruokalista')
router.register('ravintovaikutus', RavinVaikutuViewset, 'ravintovaikutus')
router.register('perustiedot', PerustiedotViewset, 'perustiedot')


urlpatterns = [
    url("^", include(router.urls)),
    url("^auth/register/$", RegistrationAPI.as_view()),
    url("^auth/change/$", ChangePasswordAPI.as_view()),
    url("^auth/login/$", LoginAPI.as_view()),
    url("^auth/logout/$", LogoutView.as_view(), name="knox_logout"),
    url("^auth/user/$", UserAPI.as_view()),
]