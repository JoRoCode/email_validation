from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User

@app.route('/users')
def index():
    users = User.get_all_users()
    print(users)
    return render_template('index.html', users=users)


@app.route('/user/new', methods=["GET"])
def new_user():
    return render_template('create.html')

@app.route('/user/create', methods=["POST"])
def create_user():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }
    user_id = User.create_user(data)
    if not User.validate_user(request.form):
        return redirect('/user/new')
    return redirect(f'/user/{user_id}')

@app.route('/user/<int:user_id>')
def show(user_id):
    user = User.show_user(user_id)
    return render_template('show.html', user=user)

@app.get('/users/<int:user_id>/edit')
def edit(user_id):
    user = User.show_user(user_id)
    print(user, '!!!~!!!!!!!!!')
    return render_template('edit.html', user=user)

@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    User.edit_user(request.form)
    return redirect(f'/user/{user_id}')

@app.route('/users/delete/<int:user_id>')
def delete(user_id):
    User.delete(user_id)
    return redirect('/users')
