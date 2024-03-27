#!/usr/bin/python3
from flask import flash, render_template, url_for, redirect, session, request
from forms.login_resgistration import (RegistrationForm, LoginForm, LogOutForm,
                                       UpdateProfile)
from forms.question_form import QuestionForm, EditPostForm
from web_flask import (app, save_image_to_db, login_manager)
from models.user import User
from models.question import Question
from models.answer import Answer
from hashlib import md5
from uuid import uuid4
from models import storage
from flask_login import login_required, current_user, login_user, logout_user, user_logged_in, user_logged_out
from random import randint
from forms.answer_form import CommentForm, EditCommentForm


@login_manager.user_loader
def load_user(id):
    user_data = storage.get(User, id)
    if user_data:
        return user_data
    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created succesfully!', category='message')
        info = {
            'full_name': form.full_name.data,
            'email': form.email.data,
            'password': form.password.data,
            'username': form.username.data,
            'gender': form.gender.data,
        }
        gender = form.gender.data
        image = save_image_to_db(image_file='default.png')[0]
        image_fmt = 'png'
        if gender == 'Male':
            image = save_image_to_db(image_file='man.jpg')[0]
            image_fmt = 'jpg'
        if gender == 'Female':
            image = save_image_to_db(image_file='woman.jpg')[0]
            image_fmt = 'jpg'
        info.update(**{'image': image, 'image_fmt': image_fmt})
        user = User(**info)
        storage.new(user)
        storage.save()
        return redirect(url_for('login'))
    return render_template('register.html', register=form, title='SignUp', cache_id=uuid4())


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('new_feed'))

    if login.validate_on_submit():
        username = login.username.data
        password = login.password.data
        user = storage.get_user(User, username)
        if user and user.password == md5(password.encode('utf-8')).hexdigest():
            login_user(user)
            return redirect(url_for('new_feed'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
    return render_template('login.html', login=login, title='Sign In', cache_id=uuid4())


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def ask_question():
    user_info = current_user.to_dict()
    ask_question = QuestionForm()
    if ask_question.validate_on_submit():
        question_detail = {
            'user_id': user_info['id'],
            'title': ask_question.title.data,
            'question': ask_question.question.data,
        }
        question = Question(**question_detail)
        storage.new(question)
        storage.save()
        return redirect(url_for('my_post'))
    return render_template('new_post.html', ask_question=ask_question,  a=True, nav=True)


@app.route('/edit/<question_id>', methods=['GET', 'POST'])
@login_required
def edit(question_id):
    edit_form = EditPostForm()
    question_object = storage.get(Question, question_id)
    question_object_dict = question_object.to_dict()
    edit_form.title.data = question_object_dict['title']
    edit_form.question.data = question_object_dict['question']
    if edit_form.validate_on_submit():
        question_object.title = request.form['edit-post-title']
        question_object.question = request.form['edit-question-area']
        storage.save()
        return redirect(url_for('my_post'))
    return render_template('edit_post.html', edit_form=edit_form, question_id=question_id, a=True, nav=True)


@app.route('/read_post/<question_id>', methods=['GET', 'POST'])
def read_post(question_id):
    question_object = storage.get(Question, question_id)
    session['question_id'] = question_object.id
    comments = storage.get_comments(Answer, question_id)
    sorted_comments = []
    if comments:
        sorted_comments = sorted(
            [comment for comment in comments], key=lambda x: x[1].created_at)
    comment_form = CommentForm()
    user_id = current_user.id
    # Take comment
    if request.method == 'POST':
        if 'comment' in request.form:
            if comment_form.validate_on_submit():
                answer_detail = {
                    'user_id': current_user.id,
                    'post_id': question_id,
                    'comment': comment_form.comment.data,
                    'like': 0
                }
                answer_obj = Answer(**answer_detail)
                storage.new(answer_obj)
                storage.save()
                return redirect(url_for('read_post', question_id=question_id))
    return render_template('read_post.html', post=question_object,
                           comments=sorted_comments, nav=True, a=True, comment_form=comment_form, question_id=question_id, user_id=user_id,
                           cache_id=uuid4())


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    c_user = current_user.to_dict()
    user_obj = storage.get(User, c_user['id'])
    update_profile = UpdateProfile()

    update_profile.username.data = c_user['username']
    update_profile.full_name.data = c_user['full_name']
    update_profile.email.data = c_user['email']
    update_profile.gender.data = c_user['gender']
    update_profile.image.data = user_obj.image

    # Update profile
    if 'edit-profile-btn' in request.form:
        if update_profile.validate_on_submit():
            request_form = request.form
            user_obj.username = request_form['username']
            user_obj.full_name = request_form['full_name']
            user_obj.email = request_form['email']
            user_obj.gender = request_form['gender']
            image_file = request.files.get('image')
            if image_file:
                updated_byte = save_image_to_db(
                    image_file, is_file_storage=False)
                user_obj.image = updated_byte[0]
                user_obj.image_fmt = updated_byte[1]
            storage.save()
            return redirect(url_for('profile'))

    return render_template('edit_profile.html', profile=update_profile, user=user_obj, nav=True, a=True)


@app.route('/')
@app.route('/home')
@app.route('/new_feed', methods=['GET', 'POST'])
@login_required
def new_feed():
    all_questions = storage.all(Question)
    gt = storage.get_other_question(User, current_user.id)
    user = storage.get(User, current_user.id)
    loader = [v.to_dict() for v in all_questions.values() if v.to_dict()['user_id'] !=
              current_user.id or []]
    sorted_questions = []
    if gt:
        sorted_questions = sorted(
            [q for q in gt], key=lambda x: x[0].created_at, reverse=True)
    get_users = [storage.get(User, user['user_id'])
                 for user in loader or []]
    return render_template('new_feed.html', questions=sorted_questions, nav=True, users=get_users, user=user, title='New Feed')


@app.route('/my_post', methods=['GET', 'POST'])
@login_required
def my_post():
    user_credential = current_user.to_dict()

    user = storage.get_user(User, user_credential['username'])
    loader = storage.get_questions(Question, user_credential['id'])

    # Sorting question in an ascending order
    load_questions = [obj.to_dict() for obj in loader or []]
    sorted_questions = []
    if load_questions:
        sorted_questions = sorted(
            load_questions, key=lambda x: x['created_at'], reverse=True)

    return render_template('my_post.html', info=user_credential, user=user, cache_id=uuid4(),
                           title='Home', questions=sorted_questions, nav=True)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    logout = LogOutForm()
    user = storage.get(User, current_user.id)
    # Log user out
    if 'logout' in request.form:
        if logout.validate_on_submit():
            logout_user()
            return redirect(url_for('login'))
    return render_template('profile.html', nav=True, user=user, logout=logout, title='Profile')


@app.route('/edit_comment/<answer_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(answer_id):
    edit_cmt = EditCommentForm()
    answer_obj = storage.get(Answer, answer_id)
    edit_cmt.edit_comment.data = answer_obj.comment
    if 'submit-edit-btn' in request.form:
        if edit_cmt.validate_on_submit():
            answer_obj.comment = request.form['edit-comment']
            storage.save()
            return redirect(url_for('read_post', question_id=answer_obj.post_id))

    return render_template('edit_comment.html', edit=edit_cmt, answer_id=answer_id, nav=True, a=True, cache_id=uuid4())


@app.route('/delete-comment/<comment_id>', methods=['DELETE', 'POST', 'GET'])
@login_required
def delete_comment(comment_id):
    comment = storage.get(Answer, comment_id)
    storage.delete(comment)
    storage.save()

    # Respond with a success message
    return redirect(url_for('read_post', question_id=session['question_id']))


@app.route('/delete-question/<question_id>', methods=['DELETE', 'POST', 'GET'])
@login_required
def delete_post(question_id):
    question_obj = storage.get(Question, question_id)
    storage.delete(question_obj)
    storage.save()

    # Respond with a success message
    return redirect(url_for('my_post'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=randint(2000, 8000), debug=True)
