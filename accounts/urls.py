from django.urls import include, re_path as path

from .views import (

    SendCoupon,
)


urlpatterns = [
    path(r'cupon$', SendCoupon.as_view(), name="cupon"),

]
