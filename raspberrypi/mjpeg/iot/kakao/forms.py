from django import forms
import json
import requests

class KakaoTalkForm(forms.Form):
    text = forms.CharField(label='전송할 Talk', max_length=300)
    web_url = forms.CharField(label='Web URL', max_length=300,
                            initial='http://172.30.1.57:8000/mjpeg/snapshot')
    mobile_web_url = forms.CharField(label='Mobile URL', max_length=300,
                            initial='http://172.30.1.57:8000/mjpeg/snapshot')

    def send_talk(self):
        talk_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        with open("/home/pi/.access_token.txt", "r") as f:
            token = f.read()
        header = {"Authorization": f"Bearer {token}"}
        # text_template = {
        #     'object_type': 'text',
        #     'text': self.cleaned_data['text'],
        #     'link': {
        #         'web_url': self.cleaned_data['web_url'],
        #         'mobile_web_url': self.cleaned_data['mobile_web_url']
        #     }
        # }
        # print(text_template)

        template_object = {
            'object_type': 'feed',
            'content':{
                'title': self.cleaned_data['text'],
                'description': self.cleaned_data['text'],
                "image_url": "http://172.30.1.57:8000/mjpeg/snapshot",
                "image_width": 640,
                "image_height": 640,
                "link": {
                    "web_url": "http://172.30.1.57:8000/mjpeg/stream",
                    "mobile_web_url": "http://172.30.1.57:8000/mjpeg/stream",
                    # "android_execution_params": "contentId=100",
                    # "ios_execution_params": "contentId=100"
                    }
                },
            "social": {
                "like_count": 100,
                "comment_count": 200,
                "shared_count": 300,
                "view_count": 400,
                "subscriber_count": 500
                },
            "buttons": [
                {
                    "title": "웹으로 이동",
                    "link": {
                        "web_url": "http://www.daum.net",
                        "mobile_web_url": "http://m.daum.net"
                        }
                },
                {
                    "title": "앱으로 이동",
                    "link": {
                        "android_execution_params": "contentId=100",
                        "ios_execution_params": "contentId=100"
                    }
                }
            ]
        }
        payload = {'template_object': json.dumps(template_object)}
        res = requests.post(talk_url, data=payload, headers=header)
        return res, self.cleaned_data['text']