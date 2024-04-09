#!/usr/bin/python3
from flask import flash, render_template, url_for, redirect, session, request, abort
from forms.login_resgistration import (RegistrationForm, LoginForm,
                                       UpdateProfile)
from forms.question_form import QuestionForm, EditPostForm
from forms.reset_forms import RequestResetForm, ResetPasswordForm
from web_flask import (app, save_image_to_db, login_manager,
                       send_reset_email, Image, BytesIO, timeConversion)
from models.user import User
from models.post import Post
from models.comment import Comment
from pathlib import Path
from uuid import uuid4
from models import storage
from flask_login import login_required, current_user, login_user, logout_user
from forms.answer_form import CommentForm, EditCommentForm, LikeForm
from datetime import timedelta
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

"""TalkIT application has the following router:
1. /register - To registration page
2. /login - To log in page
3. /new_post - To creating a post
4. /edit - To editing a post
5. /read_post - To read a post
6. /edit_profile - To edit current user's profile
7. /new_feed - For other users' post
8. /my_post - For current user's post
9. /profile - To current user profile
10. /edit_comment - To edit comment
11. /delete_comment - For user to delete a comment
12. /delete_post - To deleting a current user post
13. /reset_request - To requesting for reseting a password
14 /reset_token/<token> - To resetting password using generated token
15. /home - To landing page
16. /developer - To deveolper page
"""


@login_manager.user_loader
def load_user(id):
    '''Load user'''
    user_data = storage.get(User, id)
    if user_data:
        return user_data
    return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Registration'''
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
    '''Login'''
    login = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('new_feed'))

    if login.validate_on_submit():
        username = login.username.data
        user = storage.get_user(User, username)
        login_user(user, login.remember_me.data, timedelta(days=10))
        return redirect(url_for('new_feed'))
    return render_template('login.html', login=login, title='Sign In', cache_id=uuid4())


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def ask_question():
    '''Creating a new post'''
    user_info = current_user.to_dict()
    ask_question = QuestionForm()

    if ask_question.validate_on_submit():
        question_detail = {
            'user_id': user_info['id'],
            'title': ask_question.title.data,
            'question': ask_question.question.data,
        }
        images = request.files.getlist('post-images')
        question = Post(**question_detail)
        # Post images
        if images and images[0].filename:
            question.post_images = [
                f'post-images/{question.id}/{image.filename}' for image in images]
            for image in images:
                try:
                    path = Path(f'web_flask/static/post-images/{question.id}')
                    path.mkdir(mode=511, exist_ok=True)
                    img = Image.open(BytesIO(image.read()))
                    img.thumbnail((700, 700))
                    img.save(path.joinpath(image.filename))
                except Exception as e:
                    print(e)
        storage.new(question)
        storage.save()
        return redirect(url_for('my_post'))
    return render_template('new_post.html', ask_question=ask_question, nav=True, a=True)


@app.route('/edit/<question_id>', methods=['GET', 'POST'])
@login_required
def edit(question_id):
    '''Editing a post based on post_id'''
    edit_form = EditPostForm()
    question_object = storage.get(Post, question_id)
    if question_object is None:
        return abort(404)
    question_object_dict = question_object.to_dict()
    edit_form.title.data = question_object_dict['title']
    edit_form.question.data = question_object_dict['question']
    if edit_form.validate_on_submit():
        question_object.title = request.form['edit-post-title']
        question_object.question = request.form['edit-question-area']
        storage.save()
        return redirect(url_for('my_post'))
    return render_template('edit_post.html', edit_form=edit_form, question_id=question_id, nav=True, a=True)


@app.route('/read_post/<question_id>', methods=['GET', 'POST'])
def read_post(question_id):
    '''Read a post based on post_id selected/clicked'''
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    question_object = storage.get(Post, question_id)

    if question_object is None:
        return abort(404)
    session['question_id'] = question_object.id
    comments = storage.get_comments(Comment, question_id)
    sorted_comments = []
    time_created = []
    if comments:
        sorted_comments = sorted(
            [comment for comment in comments], key=lambda x: x[1].created_at)
        time_created = [a[1].to_dict()['created_at_time']
                        for a in sorted_comments]

    comment_form = CommentForm()
    form = LikeForm()
    user_id = current_user.id

    current_user.checked = False
    if request.method == 'POST':
        # Take comment
        if 'comment' in request.form:
            if comment_form.validate_on_submit():
                answer_detail = {
                    'user_id': current_user.id,
                    'post_id': question_id,
                    'comment': comment_form.comment.data,
                    'like': 0
                }
                answer_obj = Comment(**answer_detail)
                storage.new(answer_obj)
                storage.save()
                return redirect(url_for('read_post', question_id=question_id))
        # Take likes
        if 'like' in request.form:
            if form.validate():
                if not question_object.has_liked:
                    question_object.likes += 1
                    question_object.has_liked = True
                else:
                    question_object.likes -= 1
                    question_object.has_liked = False
                storage.save()
                return redirect(url_for('read_post', question_id=question_id))

    total_comment = storage.count_comment(question_id)

    return render_template('read_post.html', post=question_object,
                           comments=sorted_comments, nav=True, a=True, comment_form=comment_form, question_id=question_id, user_id=user_id,
                           cache_id=uuid4(), read=True, total_comment=total_comment, like=form, title='Reading...',
                           time_created=time_created)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    '''Edit a current user profile'''
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


@app.route('/new_feed', methods=['GET', 'POST'])
@login_required
def new_feed():
    '''Other users posts'''
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    all_questions = storage.all(Post)
    gt = storage.get_other_question(User, current_user.id)
    user = storage.get(User, current_user.id)
    loader = [v.to_dict() for v in all_questions.values() if v.to_dict()['user_id'] !=
              current_user.id or []]
    sorted_questions = []
    time_created = []
    if gt:
        sorted_questions = sorted(
            [q for q in gt], key=lambda x: x[0].created_at, reverse=True)
        time_created = [a[0].to_dict()['created_at_time']
                        for a in sorted_questions]
    get_users = [storage.get(User, user['user_id'])
                 for user in loader or []]
    return render_template('new_feed.html', questions=sorted_questions, nav=True, a=True, users=get_users, user=user, title='New Feed', time_created=time_created)


# My posts
@app.route('/my_post', methods=['GET', 'POST'])
@login_required
def my_post():
    '''Current user post excluding other users posts'''
    user = storage.get_user(User, current_user.username)
    loader = storage.get_questions(Post, current_user.id)

    # Sorting question in an ascending order
    load_questions = [obj.to_dict() for obj in loader or []]
    sorted_questions = []
    time_created = []
    if load_questions:
        sorted_questions = sorted(
            load_questions, key=lambda x: x['created_at'], reverse=True)
        time_created = [a['created_at_time'] for a in sorted_questions]

    return render_template('my_post.html', info=current_user, user=user, cache_id=uuid4(),
                           title='My Post', questions=sorted_questions, nav=True, a=True,
                           time_created=time_created)


# Profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    '''Current user\'s profile'''
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    user = storage.get(User, current_user.id)
    return render_template('profile.html', nav=True, a=True,  user=user, logout=logout, title='Profile')


@app.route('/edit_comment/<answer_id>', methods=['GET', 'POST'])
@login_required
def edit_comment(answer_id):
    '''Edit a comment made by the current user'''
    edit_cmt = EditCommentForm()
    answer_obj = storage.get(Comment, answer_id)
    if answer_obj is None:
        return abort(404)

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
    '''Delete a comment based on comment_id'''
    comment = storage.get(Comment, comment_id)
    if comment is None:
        return abort(404)
    storage.delete(comment)
    storage.save()
    return redirect(url_for('read_post', question_id=session['question_id']))


@app.route('/delete-question/<question_id>', methods=['DELETE', 'POST', 'GET'])
@login_required
def delete_post(question_id):
    '''Allow user to delete a post based on the post_id'''
    import shutil
    question_obj = storage.get(Post, question_id)
    if question_obj is None:
        return abort(404)
    storage.delete(question_obj)
    storage.save()
    path = Path(f'web_flask/static/post-images/{question_id}')
    if path.exists() and path.is_dir():
        shutil.rmtree(path)
    return redirect(url_for('my_post'))


@app.route('/logout')
@login_required
def logout():
    '''Log out the current user'''
    logout_user()
    return redirect(url_for('login'))


@app.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    '''Request password reset'''
    if current_user.is_authenticated:
        return redirect(url_for('new_feed'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = storage.get_user_by_email(User, form.email.data)
        send_reset_email(user)
        flash('An email has been sent with the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form, title='Reset Password', a=True)


@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    '''Request password reset'''
    if current_user.is_authenticated:
        return redirect(url_for('new_feed'))
    user = User.verify_reset_token(storage, User, token)
    form = ResetPasswordForm()
    if user is None:
        flash('That is an invalid or expired token')
        return redirect(url_for('request_reset'))
    if form.validate_on_submit():
        from hashlib import md5
        user.password = md5(form.password.data.encode()).hexdigest()
        flash('Password has been changed successfully!')
        storage.save()
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form, token=token)


@app.errorhandler(404)
def url_not_found(error):
    '''Not found page'''
    return render_template('page_not_found.html', title='Page not found'), 404


@login_manager.unauthorized_handler
def unauthorized_user():
    '''Handling unauthorized user'''
    return redirect(url_for('login'))


@app.route('/')
@app.route('/about')
def home():
    '''About page rendering if user is authenticated, Home page if not'''
    is_authorized = False
    title = None
    nav_link = False
    if not current_user.is_authenticated:
        is_authorized = True
    else:
        title = 'About'
        nav_link = True
    return render_template('landing_page.html', nav=True, title=title, sign_in_up=is_authorized, a=nav_link)


@app.route('/developer')
def developer():
    '''Rendering Developer page'''
    is_authorized = False
    nav_link = False
    if not current_user.is_authenticated:
        is_authorized = True
    else:
        nav_link = True
    return render_template('developer.html', nav=True, title='Developer', sign_in_up=is_authorized, a=nav_link, dev=True)


@app.route('/other_user_profile/<other_user_username>')
def other_user_profile(other_user_username):
    other_user = storage.get_user(User, other_user_username)
    if other_user is None:
        return abort(404)
    loader = storage.get_questions(Post, other_user.id)

    # Sorting question in an ascending order
    load_questions = [obj.to_dict() for obj in loader or []]
    sorted_questions = []
    if load_questions:
        sorted_questions = sorted(
            load_questions, key=lambda x: x['created_at'], reverse=True)
    return render_template('other_user_profile.html', user=other_user, other_u_username=other_user_username, nav=True, title=f'{other_user_username} Profile', cache_id=uuid4(),
                           questions=sorted_questions, a=True)


if __name__ == '__main__':
    from random import randint
    app.run(port=randint(2000, 9000), debug=True)
