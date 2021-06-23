import pycurl
from io import BytesIO 
from urllib.parse import urlencode
import json
import os


class PaymentsCityBank():

    def __init__(self, curl_post, service_url, proxy, proxyauth):
        self.curl_post = curl_post
        self.service_url = service_url
        self.proxy = proxy
        self.proxyauth = proxyauth
    
    def executePayment(self):
        try:
            b_obj = BytesIO()
            crl = pycurl.Curl() 
            module_dir = os.path.dirname(__file__)
            createorder__crt = os.path.join(module_dir, 'createorder.crt')
            createorder__key = os.path.join(module_dir, 'createorder.key')
            #postfields = '{"password": "123456Aa","userName": "test"}'
            headers = ["Content-Type:application/json"]
            crl.setopt(crl.URL, self.service_url)
            crl.setopt(crl.HTTPHEADER, headers)
            crl.setopt(crl.SSL_VERIFYPEER, False)
            crl.setopt(crl.SSL_VERIFYHOST, False)
            crl.setopt(crl.SSLCERT, createorder__crt)
            crl.setopt(crl.SSLKEY, createorder__key)
            crl.setopt(crl.POSTFIELDS, self.curl_post)
            # Write bytes that are utf-8 encoded
            crl.setopt(crl.WRITEDATA, b_obj)
            # Perform a file transfer 
            crl.perform() 
            # End curl session
            crl.close()
            # Get the content stored in the BytesIO object (in byte characters) 
            get_body = b_obj.getvalue()
            # Decode the bytes stored in get_body to HTML and print the result    
            return get_body.decode('utf8')
        except Exception as e:
            message = "Something went wrong." + str(e)
            print( "Exception: " + str(e))
