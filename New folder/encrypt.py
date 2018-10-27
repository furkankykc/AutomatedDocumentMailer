# Inspired from http://coding4streetcred.com/blog/post/Asymmetric-Encryption-Revisited-(in-PyCrypto)
# PyCrypto docs available at https://www.dlitz.net/software/pycrypto/api/2.6/

from Crypto import Random
from Crypto.PublicKey import RSA
import base64

def generate_keys():
	# RSA modulus length must be a multiple of 256 and >= 1024
	modulus_length = 256*4 # use larger value in production
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

a_message = "The quick brown fox jumped over the lazy dog"
privatekey , publickey = generate_keys()
encrypted_msg = encrypt_message(a_message.encode('utf-8') , publickey)
decrypted_msg = decrypt_message(encrypted_msg, privatekey)

print("%s - (%d)" % (privatekey.exportKey().decode('utf-8') , len(privatekey.exportKey())))
print("%s - (%d)" % (publickey.exportKey().decode('utf-8') , len(publickey.exportKey())))
print(" Original content: %s - (%d)" % (a_message, len(a_message)))
print("Encrypted message: %s - (%d)" % (encrypted_msg.decode('utf-8'), len(encrypted_msg)))
print("Decrypted message: %s - (%d)" % (decrypted_msg.decode('utf-8'), len(decrypted_msg)))

privatekey= """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCCUctk2TxgapEUCqF2Wfe83kgIQdoEqTIvmDRludlIG4OdZPi9
LeIRXnvQ+VqylGmu+J7nu/fMIjpS7K2uySYHWGRX240EsK70I3sGH3eTw5p43iLC
G6KEsUByIqv2+A8EKVXhFjY6+/ac/OEF7GTYGrxGdYAbzhi2fgaMQGS17QIDAQAB
AoGAcxsICdWO7KJz7j3Ni5m/pgS3nwN7LC698yf+7/MNphEXWUg8I+yJB0prFpOI
tr878Z4LzSdLofSBi4kdh4qHmSagKKK76beI/C6RzohQpdPAnEVIfrSgeD1ID8L0
k9N3is/UR40OaLmhZDBMLR6tHt55EgHf7XdmWLZN3uRBaEECQQC1XS3op/ADp4Ht
ctkn6T7WLDoYof3uAYmd71s45OHX06byRCNXLO8P7vOPLhy5G+9B301avu3/jmmp
03GdoNS1AkEAt/MLeVO/PqiO/FhXculdEmjXQBvND/4z8yDqSStPbofGS9CVQcPh
2BWBSFYKk9XftknX/BklJEZ+e1Bd5HSXWQJAHmenqah14Xb0nkUxyLIeubMibjzC
IGObmaGmDmy4vAEcrOLlddjvnyE1LdzSLepT+xwfkMYPildquXDcTEvJPQJBAJou
6eskOyS1/EOfeI0k9ZI8tk9R/ivtknWznSz/VHD89UUO7ExXd7G7NMYA+JS5q+4L
LzJrkSo6vEF4N3sKDuECQQCzkWcjDq+xTmPCPFtwMs53QmDHbheXAAkH6CO8zysB
zpVt3WeuJw9DbQyUfFQ4SWmidBT8Qj6mMqM3tpswuhhK
-----END RSA PRIVATE KEY-----"""
myEncryped="""cy4eQj7ltxqDR5IDoRdFh0tMNSNE2Iuue4pZ1el2fKcE3IL41QsIwqD46fqVr0dxF3R+t8hQImNpLfTDTiJPzlA+o4nQzPR9Ujykg0fQep19VoewYHzfXXJMV1+rzcmsCbj34Kh/KkSBN2M8h1uQ2lPJiaVm3s3dxa0jUc1QDK8="""
decrypted_msg = decrypt_message(myEncryped, RSA.importKey(privatekey.encode('utf-8')))
print(decrypted_msg)