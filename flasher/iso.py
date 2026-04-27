import shutil

def convert_iso_to_img(iso_path):
    img_path = iso_path.replace(".iso", ".img")
    shutil.copyfile(iso_path, img_path)
    return img_path
