import os
import secrets
from PIL import Image
from flask import url_for, current_app

def save_item_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)

    return picture_fn
