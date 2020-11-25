import requests, urllib, time
from django.conf import settings

class SmsWireless():
    
    def __init__(self,msisdn, body):
        self.msisdn = msisdn
        self.body = body
    def sendSMSWithGet(self):
        params = SmsWireless.getParams(self.msisdn, self.body)
        response = requests.get('https://sms.sslwireless.com/pushapi/dynamic/server.php', params=params)
        return response.text
    
    
    def sendSMSWithPost(self):
        params = SmsWireless.getParams(self.msisdn, self.body)
        response = requests.post('https://sms.sslwireless.com/pushapi/dynamic/server.php', params=params)
        return response.text

    @staticmethod
    def getParams(msisdn, body):
        params = {
            'user': settings.SMS_CONFIG['username'],
            'pass': settings.SMS_CONFIG['password'],
            'sid': settings.SMS_CONFIG['sid'],
            'sms': body,
            'msisdn': msisdn,
            'csmsid': str(round(time.time() * 1000)),
        }
        urllib.parse.urlencode(params)
        return params