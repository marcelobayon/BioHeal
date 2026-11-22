# BioHeal teaching example — standard library only.
# See docs/biological-computing-theory.md for the full discussion.

"""Example I — Malware signature lookup (immune recognition)."""
import hashlib

KNOWN_BAD_SHA256 = {
    # Demonstration placeholder only; do not treat this as a real threat feed.
    "0000000000000000000000000000000000000000000000000000000000000000"
}


def sha256_hex(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def is_known_signature(content: bytes) -> bool:
    return sha256_hex(content) in KNOWN_BAD_SHA256


if __name__ == "__main__":
    print("known:", is_known_signature(b"hello"))
