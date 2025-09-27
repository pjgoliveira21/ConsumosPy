from PIL import Image, ImageTk, ImageOps

def resize_icon(path, size):
    """Redimensiona mantendo proporção."""
    img = Image.open(path)
    img = ImageOps.contain(img, size)
    return ImageTk.PhotoImage(img)
