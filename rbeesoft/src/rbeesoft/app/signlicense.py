import base64
import argparse
import json
import time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

def canonical_json_bytes(obj: dict) -> bytes:
    # Deterministic JSON -> same bytes everywhere
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")

def load_private_key(path: Path) -> Ed25519PrivateKey:
    key_bytes = path.read_bytes()
    return Ed25519PrivateKey.from_private_bytes(key_bytes)

def make_license_payload(
    customer: str,
    product: str,
    expires_days_from_now: int,
    features: list[str],
    machine_fp: str | None = None,
) -> dict:
    now = int(time.time())
    exp = now + expires_days_from_now * 24 * 3600
    payload = {
        "customer": customer,
        "product": product,
        "features": features,
        "issued_at": now,
        "exp": exp,
        "license_id": f"LIC-{now}",
    }
    # Optional machine binding (keep None for portable)
    if machine_fp:
        payload["machine_fp"] = machine_fp
    return payload

def sign_license(payload: dict, priv: Ed25519PrivateKey) -> dict:
    msg = canonical_json_bytes(payload)
    sig = priv.sign(msg)
    return {
        "payload": payload,
        "signature": base64.b64encode(sig).decode("ascii"),
        "alg": "Ed25519",
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('private_key_path', help='Path to private key file')
    parser.add_argument('output_dir', help='Path to output directory where license.json is written')
    parser.add_argument('product', help='Name of product')
    parser.add_argument('expires_days_from_now', help='Number of days to expire', type=int)
    args = parser.parse_args()
    priv_path = Path(args.private_key_path) # Path.home() / 'keys/ed25519_private.key'
    out_path = Path(args.output_dir) # 'license.json'
    priv = load_private_key(priv_path)
    payload = make_license_payload(
        customer='Default customer',
        product=args.product,
        expires_days_from_now=args.expires_days_from_now,
        features=[],
        machine_fp=None,  # set to a fingerprint to bind to a device
    )
    signed = sign_license(payload, priv)
    out_path.write_text(json.dumps(signed, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote signed license to: {out_path.resolve()}")
    print(f"Expires at (unix): {payload['exp']}")

if __name__ == "__main__":
    main()
