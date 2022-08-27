from django.conf import settings
from allauth.socialaccount.models import SocialAccount, SocialApp
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import requests
from rest_framework import status
from json.decoder import JSONDecodeError
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from .serializers import UserSerializer
import os
User = get_user_model()

state = os.environ.get('STATE')

BASE_URL = 'http://127.0.0.1:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'api/accounts/google/callback/'



def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    # "구글 로그인: 스코프", scope, "클라이언트 아이디", client_id
    # "리턴URI :",f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

    
def google_callback(request):
    # "콜백", request
    client_id = os.environ.get("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get('code')
    
    # "구글 콜백 클라이언트 아이디:", client_id, "클라이언트 시크릿:", client_secret, "코드:", code)
    """
    Access Token Request
    """
    # "구글 콜백 URI: ", GOOGLE_CALLBACK_URI
    # "인증 주소:", f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}"
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    # "콜백 토큰 리퀘스트 제이슨: token_req_json
    if error is not None:
        # "JSON 디코드 에러")
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')
    id_token = token_req_json.get('id_token')

    # "엑세스 토큰: ", access_token
    # "아이디 토큰: ", id_token
    """
    Profile Request
    """
    
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        params={
            'access_token': access_token
        }
    )
    user_info = user_info_response.json()
    # 프로필 가져오기 user_info
    name = user_info['name']
    email = user_info['email']
    #given_name, picture
    
    """
    Signup or Signin Request
    """
    try:
        # 기존 유저 있음
        user = User.objects.get(email=email)
        
        
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        # 소셜 유저: social_user
        if social_user is None:
            # 소셜 유저 없음
            return JsonResponse({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        if social_user.provider != 'google':
            # 구글이 아님
            return JsonResponse({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
        # 기존에 Google로 가입된 유저
        data = {'access_token': access_token, 'code': code, 'id_token': id_token}
        # 넘어온 데이터 data
        
        serializer = UserSerializer(user, many=False)
        return JsonResponse({'user': serializer.data, 'data': data, 'new': False})

    except:
        # 기존 유저 없음
        # 기존에 가입된 유저가 없으면 새로 가입
        user = User.objects.create(
            email = email,
            name = name
        )
        
        provider = SocialApp.objects.get(provider='google')
        # 유저 생성
        socialaccont = SocialAccount.objects.create(
            user = user,
            provider = provider,
            uid = user.id
        )
        # 소셜 어카운트 생성 socialaccont

        
        data = {'access_token': access_token, 'code': code, 'id_token': id_token}
        serializer = UserSerializer(user, many=False)
        return JsonResponse({'user': serializer.data, 'data': data, 'new': True})


class GoogleLogin(SocialLoginView):
    # 구글 로그인 소셜 로그인 뷰
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client



@permission_classes([IsAuthenticated])
@api_view(['PATCH'])
def editname(request):
    data = request.data
    user = request.user

    try:
        user = User.objects.get(user=user)
        user.name = data['name']
        user.save()

        serializer = UserSerializer(user, many=False)

        return Response({'post': serializer.data, 'message': "EDITED"})
    except:
        return Response({'message': "UNAUTHORIZED"})