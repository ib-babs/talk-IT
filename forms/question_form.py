#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField, ValidationError
from wtforms.validators import DataRequired, Length
"""question_form module has two main classes:
    QuestionForm - For taking user post, it includes title of the post,
    and the post itself
    EditPostForm class - For editing user post
    """


class QuestionForm(FlaskForm):
    '''Flask form subclass'''
    title = StringField(validators=[DataRequired(
    )], id='question_title', name='question_title', render_kw={'placeholder': 'Title'})

    question = TextAreaField(validators=[DataRequired(
    )], id='question-area', name='question-area', render_kw={'placeholder': 'Your question goes here', 'cols': 80, 'rows': 22})
    post_images = MultipleFileField(render_kw={
                                    'accept': 'image/*', 'class': 'post_images'}, id='post-images', name='post-images', validators=[Length(1, 10)])

    def validate_post_images(self, post_images):
        if len(post_images.data) > 10:
            raise ValidationError(f'Maxiumun of 10 images. {len(post_images.data)} are selected')

    post = SubmitField('Post', id='post-btn')


class EditPostForm(FlaskForm):
    '''Form to edit a post based on post ID'''

    title = StringField(validators=[DataRequired(
    )], id='edit-post-title', name='edit-post-title')

    question = TextAreaField(validators=[DataRequired(
    )], id='edit-question-area', name='edit-question-area', render_kw={'cols': 80, 'rows': 22})
    done = SubmitField('Done', id='edit-post-btn')
