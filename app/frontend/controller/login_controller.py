from flask import Blueprint, request, redirect, render_template, url_for
from app.backend.models.user_model import UserModel
from app.frontend.models.user_login_model import UserLogin
from ..extensions import login_manager
from app.frontend.forms.form_auth import FormLogin

login = Blueprint('login', __name__, url_prefix='/', template_folder='../templates/')

@login_manager.user_loader
def load_user(user_id):
    user = UserLogin()
    user.id = user_id
    return user


@login.get('/')
def login_index():
    form = FormLogin(request.form)
    user = UserModel.id
    print(f'id user == {user}')
    return render_template('auth/login.html', form=form)

@login.route('sign-in', methods=['GET','POST'])
def masuk():
    form = FormLogin(request.form)
    
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form.get('username') 
        password = request.form.get('password') 
        
        print(username)
        print(password)
        if username and password:
            return redirect(url_for('admin2.index'))
        else:
            return redirect(url_for('login.login_index'))
    return render_template('auth/login.html', form=form)