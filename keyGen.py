from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def generatekeypair():

    private_key = ec.generate_private_key(ec.SECP256R1())

    public_key = private_key.public_key()

    return private_key, public_key

def export_private_key(private_key, password=None):

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(password.encode()) if password else serialization.NoEncryption()
    )

    return private_key_pem

def export_public_key(public_key):

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return public_key_pem
