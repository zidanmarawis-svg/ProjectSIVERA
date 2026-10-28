# routes/auth.py
# Autentikasi dan decorator role.
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, AuditLog

auth_bp = Blueprint('auth', __name__)


def role_required(role):
    """Decorator untuk membatasi akses berdasarkan role."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            db.session.add(AuditLog(user_id=user.id, aksi='login'))
            db.session.commit()
            return redirect(url_for('index'))
        flash('Username atau password salah')
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))