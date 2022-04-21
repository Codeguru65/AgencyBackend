import re
# from product.views import remove_emoji
from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.views import View
from .serializers import RegisterSerializer, SetNewPasswordSerializer, \
    EmailVerificationSerializer, LoginSerializer, LogoutSerializer, RegisterInstitutionSerializer, \
    ResetPasswordEmailRequestSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRenderer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponsePermanentRedirect, JsonResponse
import os
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.template import Template

# from rest_framework_jwt.utils import jwt_decode_handler
class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


def remove_emoji(text):
    emoji_pattern = re.compile(
        u'(\U0001F1F2\U0001F1F4)|'  # Macau flag
        u'([\U0001F1E6-\U0001F1FF]{2})|'  # flags
        u'([\U0001F600-\U0001F64F])'  # emoticons
        "+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)


@permission_classes((AllowAny,))
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        print(user,'ndiri pano')
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        otp = 'password123*'
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)

        print(f'current_site -> {current_site},  relativeLink -> {relativeLink}')
        print(absurl)
        ctx = {
            'user': user.email,
            'url': absurl,
            'otp': otp
        }
        message = get_template('mail/mail.html').render(ctx)
        email_body = message
        # email_body = 'Hi '+user.username + \
        #     ' Kindly click the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'from_email': 'chamu.nziradzemhuka@fbc.co.zw',
                'email_subject': 'Yako Portal - Verify your email'}
        response = {
            "token": "%s" % token,
            "credentials": user_data
        }
        email_body.content_subtype = 'text/html'
        # print(data)
        Util.send_email(data)
        return Response(response, status=status.HTTP_201_CREATED)

@permission_classes((AllowAny,))
class DeleteUser(views.APIView):
    
    def delete(self, request, id):
        user = get_object_or_404(User.objects.all(), id=id) 
        print(user.delete())
        
        res = {
            'res':f'user {user} deleted'
        }

        return JsonResponse(res, safe=False)
        



@permission_classes((AllowAny,))
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        # area_code = request.GET.get('area_code')
        # country = request.GET.get('country')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            print(payload, 'im the user')
            #             payload = jwt_decode_handler(token)
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                # user.area_code = area_code
                # user.country = country
                user.save()
            return redirect('/auth/welcome/')
            # return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class GetUser(views.APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            #             payload = jwt_decode_handler(token)
            user = User.objects.get(id=payload['user_id'])
            if user.is_verified:
                return Response({'response': 'Verified User'}, status=status.HTTP_200_OK)
            else:
                return Response({'response': 'User Not Verified'}, status=status.HTTP_412_PRECONDITION_FAILED)
        except:
            return Response({'error': 'Update Failed'}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer


    print("....................................")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://' + current_site + relativeLink + "?redirect_url=" +  redirect_url

            ctx = {
                'user': user.email,
                'url': absurl,
            }
            message = get_template('mail/reset_password.html').render(ctx)
            email_body = message
            # email_body = 'Hi '+user.username + \
            #     ' Kindly click the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'from_email': 'chamu.nziradzemhuka@fbc.co.zw',
                    'email_subject': 'Yako Portal - Reset Password'}


            # email_body = 'Hello, \n Use link below to reset your password  \n' + \
            #              absurl + "?redirect_url=" + redirect_url
            # data = {'email_body': email_body, 'to_email': user.email,
            #         'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(
                    redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url + '?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class Welcome(View):
    def get(self, request):
        return render(self.request, 'mail/redirect.html', )


@permission_classes((AllowAny,))
class RegisterInstitutionView(generics.GenericAPIView):
    serializer_class = RegisterInstitutionSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
