import json
import time
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from rbeesoft.common.exceptions import LicenseException
from rbeesoft.common.license import License
from rbeesoft.common.decorators import singleton


@singleton
class LicenseManager:
    def __init__(self, settings):
        self._file_path = None
        self._public_key = settings.get('public_key', None)
        self._major_version = settings.get_float('major_version', None)
        self._license = None

    def file_path(self):
        return self._file_path
    
    def public_key(self):
        return self._public_key
    
    def major_version(self):
        return self._major_version
    
    def license(self):
        return self._license

    def canonical_json_bytes(self, obj: dict) -> bytes:
        return json.dumps(
            obj,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False
        ).encode("utf-8")

    def check_license(self, file_path):
        if isinstance(file_path, str):
            file_path = Path(file_path)
        if not file_path.exists():
            raise LicenseException('No license found')
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
        # Major version check
        major_version = float(payload.get('major_version', -1))
        if major_version == -1:
            raise LicenseException(f'License has no major version property')
        if major_version != self.major_version():
            raise LicenseException(f'License requires version {major_version}. App version is {self.major_version()}')
        self._license = License(payload)
        return self._license