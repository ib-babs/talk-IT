#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):

    title = StringField(validators=[DataRequired(
    )], id='question_title', name='question_title', render_kw={'placeholder': 'Title'})

    question = TextAreaField(validators=[DataRequired(
    )], id='question-area', name='question-area', render_kw={'placeholder': 'Your question goes here', 'cols': 80, 'rows': 22})
    post = SubmitField('Post', id='post-btn')


class DeletePostForm(FlaskForm):
    '''Form to delete a post based on post ID'''
    post_id = StringField(render_kw={'class': 'post-ids'})
    submit = SubmitField('Delete', render_kw={'class': 'delete-button'})


class EditPostForm(FlaskForm):
    '''Form to edit a post based on post ID'''

    title = StringField(validators=[DataRequired(
    )], id='edit-post-title', name='edit-post-title')

    question = TextAreaField(validators=[DataRequired(
    )], id='edit-question-area', name='edit-question-area', render_kw={'cols': 80, 'rows': 22})
    done = SubmitField('Done', id='edit-post-btn')
