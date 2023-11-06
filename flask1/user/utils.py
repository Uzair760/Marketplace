import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask1 import mail
from flask_mail import Message
from flask_login import current_user


def save_picture(form_picture):
    if current_user.image_file != 'default1.jpg':
        os.remove(os.path.join(current_app.root_path, 'static/images', current_user.image_file))
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@marketplace.com', recipient=[user.email])
    msg.body = f'''To reset your password, click the following link:
{url_for('user.reset_token', token=token, _external=True)}

This link will expire in { expires_sec } seconds.

Ignore this email if you did not make this request.
    '''
    mail.send(msg)
