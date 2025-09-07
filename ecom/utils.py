# ecom/utils.py
import hmac
import hashlib
import base64
from django.conf import settings


def generate_esewa_signature(amount, transaction_uuid):

    message = f"total_amount={amount},transaction_uuid={transaction_uuid},product_code={settings.ESEWA_MERCHANT_CODE}".encode('utf-8')
    
    #
    secret = settings.ESEWA_SECRET_KEY.encode('utf-8')
    
   
    hmac_sha256 = hmac.new(secret, message, hashlib.sha256)
    
 
    signature = base64.b64encode(hmac_sha256.digest()).decode('utf-8')
    return signature