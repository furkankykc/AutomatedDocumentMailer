import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP as rsaCry


privatePEM = """-----BEGIN RSA PRIVATE KEY-----
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
-----END RSA PRIVATE KEY-----"""

def encrypt_message(message):
    global privatePEM
    message = message.encode("utf8")

    # with open('private.pem') as data:
    #     privatekey = RSA.importKey(data.read())
    privatekey = RSA.import_key(privatePEM)
    encrypted_msg = rsaCry.new(privatekey.publickey()).encrypt(message)
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)  # base64 encoded strings are database friendly
    return encoded_encrypted_msg


def decrypt_message(encodedMessage):
    global privatePEM
    print(encodedMessage)
    # encodedMessage = encodedMessage('utf8')
    # with open('private.pem') as data:
    #     privatekey = RSA.importKey(data.read())
    #     privatekey = rsaCry.new(privatekey)

    # with open('private.pem') as data:
    privatekey = RSA.importKey(privatePEM)
    privatekey = rsaCry.new(privatekey)
    decoded_encrypted_msg = base64.b64decode(encodedMessage)
    decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
    return decoded_decrypted_msg
