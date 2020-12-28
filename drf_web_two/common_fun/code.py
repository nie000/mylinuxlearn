import requests
from rest_framework import serializers


def send_msg(phone,code):
    #'17360163691'
    url='https://106.ihuyi.com/webservice/sms.php?method=Submit'
    data={
        'password':'e49265e63243b964e005dd6a93fa63b8',
        'account':'C47017264',
        'mobile':phone,
        'content':'	您的验证码是：{}。请不要把验证码泄露给其他人。'.format(code),
        'format':'json'
    }
    result=requests.post(url, data)
    data=result.json()
    if data['code']==2:
        return True
    else:
        raise serializers.ValidationError(data['msg'],code='send_error')