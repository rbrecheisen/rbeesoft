import os
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from pathlib import Path

# RUN THIS ONLY ONCE!!! You can distribute the public key to clients


def main():
    output_dir = Path.home() / 'keys'
    os.makedirs(output_dir, exist_ok=True)
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    priv_bytes = priv.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_bytes = pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    priv_file = output_dir / 'ed25519_private.key'
    priv_file.write_bytes(priv_bytes)
    pub_file = output_dir / 'ed25519_public.key'
    pub_file.write_bytes(pub_bytes)
    print("Wrote:")
    print(" - $HOME/keys/ed25519_private.key  (KEEP SECRET)")
    print(" - $HOME/keys/ed25519_public.key   (embed in app)")
    print("\nPublic key (base64) to embed:")
    print(base64.b64encode(pub_bytes).decode("ascii"))


if __name__ == '__main__':
    main()

