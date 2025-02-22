from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from .models import User, Profile
from .serializers import UserSerializer, ProfileSerializer,LoginSerializer
from rest_framework.views import APIView
from django.shortcuts import redirect,render
from rest_framework.authtoken.models import Token
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send verification email
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verification_link = f"http://127.0.0.1:8000/api/auth/verify-email/{uid}/{token}/"
        
        send_mail(
            'Verify Your Email',
            f'Click here to verify: {verification_link}',
            'noreply@blooddonation.com',
            [user.email],
            fail_silently=False,
        )

        return Response(
            {'detail': 'Verification email sent'},
            status=status.HTTP_201_CREATED
        )

class VerifyEmailView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'detail': 'Email verified successfully'})
        return Response({'detail': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            if user.is_active:
                token,_=Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return Response({'detail': 'Login successful'})
            return Response({'detail': 'Account not activated'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# class UserLogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request):
#         logout(request)
#         return Response({'detail': 'Logged out successfully'})
class LogOutApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect("login")

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile