#!/usr/bin/python3
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import SubmitField, TextAreaField


class CommentForm(FlaskForm):
    '''Comment form'''
    comment = TextAreaField(
        validators=[DataRequired()], name='comment', id='comment', render_kw={"placeholder":  'Your Comment', 'class': 'cmt-txt-area'})
    submit_comment = SubmitField(
        'Comment', name='submit-comment', id='submit-comment', render_kw={'class': 'cmt_sumit-btn'})


class EditCommentForm(FlaskForm):
    '''Edit Comment form'''
    edit_comment = TextAreaField(
        validators=[DataRequired()], name='edit-comment', id='edit-comment', render_kw={'class': 'cmt-txt-area', 'cols': 80, 'rows': 20})
    submit_edit_btn = SubmitField(
        'Edit', name='submit-edit-btn', id='submit-edit-btn', render_kw={'class': 'cmt_sumit-btn'})


class EditBioForm(FlaskForm):
    '''Profile Bio form'''
    bio = TextAreaField(
        validators=[DataRequired()], name='edit-bio', id='edit-bio', render_kw={'class': 'cmt-txt-area', 'cols': 80, 'rows': 20})
    submit_bio_btn = SubmitField(
        'DONE', name='submit-bio-btn', id='submit-bio-btn', render_kw={'class': 'cmt_sumit-btn'})
