import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as rsaCry


def encrypt_message(message):
    message = message.encode("utf8")

    with open('private.pem') as data:
        privatekey = RSA.importKey(data.read())

    encrypted_msg = rsaCry.new(privatekey.publickey()).encrypt(message)
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)  # base64 encoded strings are database friendly
    return encoded_encrypted_msg


def decrypt_message(encodedMessage):
    print(encodedMessage)
    # encodedMessage = encodedMessage('utf8')
    with open('private.pem') as data:
        privatekey = RSA.importKey(data.read())
        privatekey = rsaCry.new(privatekey)
    decoded_encrypted_msg = base64.b64decode(encodedMessage)
    decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
    return decoded_decrypted_msg
