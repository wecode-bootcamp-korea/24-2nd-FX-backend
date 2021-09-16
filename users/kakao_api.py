import requests

from django.http import JsonResponse


class KakaoApi:
    def __init__(self, kakao_access_token):
        self.kakao_access_token = kakao_access_token
        self.getting_kakao_user_info_url = 'https://kapi.kakao.com/v2/user/me'

    def get_kakao_user_info(self):
        TIMEOUT = 5

        try:
            headers     = {"Authorization": f"Bearer ${self.kakao_access_token}"}
            response    = requests.get(self.getting_kakao_user_info_url, headers=headers, timeout=TIMEOUT)

            if response.json().get('code') == -401:
                return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
            if response.json().get('code') == -10:
                return JsonResponse({'message': 'API_LIMIT_EXCEEDED'}, status=400)
            return response.json()

        except TimeoutError:
            JsonResponse({'message': 'REQUEST_TIME_OUT'}, status=408)