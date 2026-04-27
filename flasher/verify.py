import hashlib

def hash_file(path, limit=None):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        total = 0
        while True:
            chunk = f.read(4096)
            if not chunk:
                break

            h.update(chunk)
            total += len(chunk)

            if limit and total >= limit:
                break

    return h.hexdigest()


def verify_flash(image, device):
    print("🔍 Verifying (partial)...")

    size = 50 * 1024 * 1024  # 50MB test
    h1 = hash_file(image, size)
    h2 = hash_file(device, size)

    if h1 == h2:
        print("✅ Verify OK")
    else:
        print("❌ Verify FAILED")
