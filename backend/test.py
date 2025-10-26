from nacl.signing import SigningKey
sk = SigningKey.generate()
vk = sk.verify_key
print(sk.encode().hex(), vk.encode().hex())