from Crypto.Cipher import AES
import base64

msg_text = 'test some plain text here'.rjust(32)
secret_key = '1234567890123456' # create new & store somewhere safe

cipher = AES.new(secret_key.encode("utf8"),AES.MODE_OFB) # never use ECB in strong systems obviously
# encoded = base64.b64encode(cipher.encrypt(msg_text.encode("utf8")))
# ...
# print (encoded.strip())
encoded =b'msibgRhBXS/84Y3h3J2/tmySbJ6RB9pip6qWk1GlxpQ='
decoded = cipher.decrypt(base64.b64decode(encoded))
print (decoded)