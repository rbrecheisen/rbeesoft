import json
import time
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from rbeesoft.common.licenseexception import LicenseException


class LicenseManager:
    def __init__(self, public_key):
        self._file_path = None
        self._public_key = public_key

    def file_path(self):
        return self._file_path
    
    def public_key(self):
        return self._public_key

    def canonical_json_bytes(self, obj: dict) -> bytes:
        return json.dumps(
            obj,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False
        ).encode("utf-8")

    def verify(self, file_path):
        if isinstance(file_path, str):
            file_path = Path(file_path)
        try:
            signed = json.loads(file_path.read_text(encoding='utf-8'))
            payload = signed['payload']
            sig_b64 = signed['signature']
            sig = base64.b64decode(sig_b64)
            msg = self.canonical_json_bytes(payload)
            pub_bytes = base64.b64decode(self.public_key())
            pub = Ed25519PublicKey.from_public_bytes(pub_bytes)
            pub.verify(sig, msg)
            # expiry check
            now = int(time.time())
            exp = int(payload["exp"])
            if now > exp:
                raise LicenseException('License expired')
            return payload
        except Exception as e:
            raise LicenseException(f'Invalid license: {e}')