from flasher.dmg import convert_dmg

def prepare_image(path):
    path = path.lower()

    if path.endswith(".img"):
        return path

    if path.endswith(".iso"):
        print("📀 ISO detected (using directly)")
        return path

    if path.endswith(".dmg"):
        return convert_dmg(path)

    raise Exception("❌ Unsupported format")
