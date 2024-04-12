#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField, ValidationError
from wtforms.validators import DataRequired, Length
"""post_form module has two main classes:
    PostForm - For taking user post, it includes title of the post,
    and the post itself
    EditPostForm class - For editing user post
    """


class PostForm(FlaskForm):
    '''Flask form subclass'''
    post = TextAreaField(validators=[DataRequired(
    )], id='post-area', name='post-area', render_kw={'placeholder': 'Your post goes here', 'cols': 80, 'rows': 22})
    post_images = MultipleFileField(render_kw={
                                    'accept': 'image/*', 'class': 'post_images'}, id='post-images', name='post-images', validators=[Length(1, 10)])

    def validate_post_images(self, post_images):
        if len(post_images.data) > 10:
            raise ValidationError(f'Maxiumun of 10 images. {len(post_images.data)} are selected')

    submit_post = SubmitField('Post', id='post-btn')


class EditPostForm(FlaskForm):
    '''Form to edit a post based on post ID'''

    post = TextAreaField(validators=[DataRequired(
    )], id='edit-post-area', name='edit-post-area', render_kw={'cols': 80, 'rows': 22})
    done = SubmitField('Done', id='edit-post-btn')
