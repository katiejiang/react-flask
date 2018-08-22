from flask import (
    Blueprint,
    jsonify,
    request,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from app import db
from app.models import User

account = Blueprint('account', __name__)

names = { 'name': 'Katie Jiang' }

@account.route('/register', methods=['POST'])
def register():
    """
    Register a new user, and send them a confirmation email.
    """
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    email = request.json.get('email')
    password = request.json.get('password')

    if None in [first_name, last_name, email, password]:
        abort(400) # missing arguments
    if User.query.filter_by(email=email).first():
        abort(400) # existing user
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password
    )
    db.session.add(user)
    db.session.commit()

    # TODO: send confirmation email

    return jsonify({
        'user': {
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
        }
    }, 201)


@account.route('/login', methods=['POST'])
def login():
    """
    Log in an existing user.
    """
    email = request.json.get('email')
    password = request.json.get('password')

    if None in [email, password]:
        abort(400) # missing arguments
    user = User.query.filter_by(email=email).first()
    if user and user.password_hash and user.verify_password(password):
        login_user(user, remember=True) # TODO: add "remember me" field
        return jsonify({}, 200)
    else:
        abort(400) # invalid username/password combination


@account.route('/logout', methods=['GET'])
@login_required
def logout():
    # logout_user()
    print(current_user)
    return jsonify({}, 200)


@account.route('/profile', methods=['GET'])
@login_required
def manage():
    return jsonify(current_user)
