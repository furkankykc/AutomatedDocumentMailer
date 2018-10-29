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
P3X3LT85SZbfXeSpCKmhX1JDv++Abb+/6y1gYRewamRqxGMNnvEopAqIAV4yx7x39a6kFCiC+LIVwSysjNCpjgpQ9VzqdbNuD/MIVXXOnVvKTZeovfaB1rdtumdgTJ9kAhnMYecEDxOeRbo7MTk/Esina8nMKBneD/C4TKEoUevuHuZmWPxwQxLNxaF7/+LwHNVwxBYP/xd8rVISsCeLOJ9BHR67ir8vevmiHp+/OpszRx6CW52wojzNmTFnRimctslzufsyL96HiXyqm+2i3YSKRNrQn0fAwwLrxHNQRe9pa1vNr/eC0omMIYhTF4aUpVG5/tf8kUddsHvN+oAkd7M8DRYNAMMNmhlu8KX4wDOzeC2dGyQsste/aT5wAQ3XkPbUUH7tXpNTZ3wI0Eyj14DGxdMwLjUkOmhcCaZ2C8tLp69kIcaGA6x5rDrRNWGDRhC2BC7HOFVmr0vmkJX+XiWVXhWqrfLCC/qUfQF5n3IQLneTlVCc+bOpiiIrODXk9IPdjJcNJ/FQYx9bgu5MWHKvVJpc7eXlc+Ztfj83Ea9/yy1TkrX8POCFJz1+z0nUe0mTH6ueM7qaL38x9M6q+W9BlCXWTKZyYIpz2VbeIisO44Vr+KFka7eDScQ56u+acZcSfUociHpPI7Mg+hQpiZMrObYh/9+3q9tJrx+oCgg=
"""
decrypted_msg = decrypt_message(myEncryped, RSA.importKey(privatekey))
print(decrypted_msg.decode("utf8"))