# Inspired from http://coding4streetcred.com/blog/post/Asymmetric-Encryption-Revisited-(in-PyCrypto)
# PyCrypto docs available at https://www.dlitz.net/software/pycrypto/api/2.6/

from Crypto import Random
from Crypto.PublicKey import RSA
import base64

def generate_keys():
	# RSA modulus length must be a multiple of 256 and >= 1024
	modulus_length = 1024*4 # use larger value in production
	privatekey = RSA.generate(modulus_length, Random.new().read)
	publickey = privatekey.publickey()
	return privatekey, publickey

def encrypt_message(a_message , publickey):
	encrypted_msg = publickey.encrypt(a_message, 32)[0]
	encoded_encrypted_msg = base64.b64encode(encrypted_msg) # base64 encoded strings are database friendly
	return encoded_encrypted_msg

def decrypt_message(encoded_encrypted_msg, privatekey):
	decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
	return decoded_decrypted_msg

########## BEGIN ##########

a_message = """<?xml version="1.0" ?>
<properties>
	<email>x-bet@x-news.site</email>
	<password>dk4402gg}i%c</password>
	<message>/home/furkankykc/Downloads/MainFix2(1).html</message>
	<subject>Örnek Konu</subject>
	<list>/home/furkankykc/Downloads/Başlıksız e-tablo.xlsx</list>
	<start>11</start>
	<task/>
	<smtp>smtpout.europe.secureserver.net:465</smtp>
	<smtp>smtp.gmail.com:587</smtp>
	<smtp>smtp-mail.outlook.com:587</smtp>
	<smtp>mail.x-news.site:465</smtp>
</properties>
"""
# privatekey , publickey = generate_keys()
# encrypted_msg = encrypt_message(a_message.encode('utf-8') , publickey)
# decrypted_msg = decrypt_message(encrypted_msg, privatekey)
#
# print("%s - (%d)" % (privatekey.exportKey().decode('utf-8') , len(privatekey.exportKey())))
# print("%s - (%d)" % (publickey.exportKey().decode('utf-8') , len(publickey.exportKey())))
# print(" Original content: %s - (%d)" % (a_message, len(a_message)))
# print("Encrypted message: %s - (%d)" % (encrypted_msg.decode('utf-8'), len(encrypted_msg)))
# print("Decrypted message: %s - (%d)" % (decrypted_msg.decode('utf-8'), len(decrypted_msg)))

with open('private.pem') as data:
	privatekey = data.read()
	print(privatekey)

myEncryped="""
BgMNMBU+MspCS1UjLIE/2076SsCeTsTHpUIo+b/p9UoZptGxLvqqE7wLcd9h9JyAZ3MrZJQpID0gcnqf27NJ7zut4xX5vAkSnlzXoKFjNLmTa+j9DBU/+3+rxDT9HdTufQcUa9xrExoalraqYgjS69tqNrXdNh9Z1bNc8CPJvPaxKBb0wDhDcHlWzwLJTRlxMtz0wse71OnVIuIukNoOArXmo+QyTMZtxdZFAonWqbW5eO6c+jmrZEaSSJ6UH46VbPlHsEVK4r0f+zCjw9/O2ZrxzDwILDMadwlcyEHSsx+ijXbNIdWFj3c1XkL2qGgRPkCh0Fe4jYNUPRTbIBcn/5nQSrCd0dxbN5Euzt07P8PIsCQM6K5LzZzFOLuDO6tXIFiTwwzDOCV+LKDaIVEffYQbRMPsdFQdkccggzo42lOKmYc7/jPa1xjYGcBuy6fvz3QRhq098tLdKbOVwRt6FbRYx6rVUDA+nHcxY76GJbqYatFHhH4ptdOS2lcOTtk+mfchVnLJZUP2sIHiY+bkiY6YK6nszhBb5VsRiG40lsODf06eGmMLENZxOWRiI4YmkUNCoWmFr0wsfMnPD4pTktR6zFY7Qpx/ska1GON7L+t1LlVtdJp4OmEM7YL2Gb18fN4mt8LbEo+LqeSqDnCswj7PO8xygHtJ0RYmkk3iQTw=
"""

decrypted_msg = decrypt_message(myEncryped, RSA.importKey(privatekey))
print(decrypted_msg.decode("utf8"))