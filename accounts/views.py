from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from django.template.loader import render_to_string
from .authentication import PasswdTokenAuthentication
from .permissions import AllowAny
from .serializers import (
    SignUpExistsSerializer,
    SignUpMailSerializer,
    SignUpCheckSerializer,
    SignUpSerializer,
    SignInSerializer,

    SocialSignUpSerializer,
    SocialSignInSerializer,

    ProfileSerializer,
    ProfileUpdateSerializer,
    AvatarSerializer,

    ChangeSerializer,

    ResetMailSerializer,
    ResetSerializer,
)

from common.utils import send_email


class SendCoupon(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        print(request.data)

        html = render_to_string('cupon.html', {
            'name': '{} {}'.format(
                request.data.get('name', ''), request.data.get('lastName', '')) 
            })

        print(html)

        send_email(
            '¡Xtistore - Obten tu descuento!',
            html, request.data.get('email'))
        return Response(status=status.HTTP_200_OK)