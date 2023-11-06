from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, current_app
from flask1 import db
from flask1.posts.forms import PostListing
from flask1.models import Post
from flask_login import current_user, login_required
from flask1.posts.utils import save_item_picture

posts = Blueprint('posts', __name__)

@posts.route("/listing_new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostListing()
    if form.validate_on_submit():
        post = Post(item=form.item.data, desc=form.desc.data, price=form.price.data, seller=current_user)
        if form.item_picture.data:
            picture_file = save_item_picture(form.item_picture.data)
            post.item_image_file = picture_file
        db.session.add(post)
        db.session.commit()
        flash('You have listed your item.', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_listing.html', title='Sell an Item', form=form, legend='Sell an Item')

@posts.route("/listing_<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.item, post=post)

@posts.route("/listing/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.seller != current_user:
        abort(403)
    form = PostListing()
    if form.validate_on_submit():
        post.item = form.item.data
        post.desc = form.desc.data
        post.price = form.price.data
        if form.item_picture.data:
            picture_file = save_item_picture(form.item_picture.data)
            post.item_image_file = picture_file
        db.session.commit()
        flash('The listing has been updated.', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.item.data = post.item
        form.desc.data = post.desc
        form.price.data = post.price
    return render_template('create_listing.html', title='Update Listing', form=form, legend='Update Listing')

@posts.route("/listing/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.seller != current_user:
        abort(403)
    if post.item_image_file != 'default2.jpg':
        os.remove(os.path.join(current_app.root_path, 'static/images', post.item_image_file))
    db.session.delete(post)
    db.session.commit()
    flash('The listing has been removed.', 'message')
    return redirect(url_for('main.home'))
