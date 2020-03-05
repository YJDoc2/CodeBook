from flask import request, Response, Blueprint, json, session, render_template, redirect
import bcrypt
from mongoengine.errors import NotUniqueError
from models.User import User
import re

user = Blueprint('user', __name__)

salt = bcrypt.gensalt()
email_rx = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')


@user.route('/user/login', methods=['POST'])
def login():
    data = request.form.to_dict()
    if 'username' not in data or 'password' not in data or data['username'].strip() == '' or data['password'].strip() == '':
        print(data)
        return render_template('login.html', error='Please Fill All Fields')
        # * FOR API return Response(json.dumps({'Success': 'False', 'error': 'Incomplete Fields'}), mimetype="application/json", status=404)
    temp = User.objects(username=data['username'])
    if len(temp) == 0:
        return render_template('login.html', error='The Email is not registered')
        # * FOR API return Response(json.dumps({'Success': 'False', 'Error': 'User Does not Exist'}), mimetype="application/json", status=404)
    temp = temp[0]
    if bcrypt.checkpw(data['password'].encode('utf-8'), temp.password.encode('utf-8')):
        return redirect('/')
        # * FOR API return Response(json.dumps({'Success': 'True'}), mimetype="application/json", status=200)
    else:
        return render_template('login.html', error='Password Does not match')
        # * FOR API return Response(json.dumps({'Error': 'Password does not match'}), mimetype="application/json", status=400)


@user.route('/user/signup', methods=['POST'])
def signup():
    data = request.form.to_dict()
    print(data)
    if 'email' not in data or 'password' not in data or 'username' not in data or 'password1' not in data \
            or data['email'].strip() == '' or data['password'].strip() == '' or data['username'].strip() == '':
        return render_template('signup.html', error='Please Fill All Fields')
        # * FOR API return Response(json.dumps({'Success': 'False', 'error': 'Incomplete Fields'}), mimetype="application/json", status=404)
    if not email_rx.match(data['email']):
        return render_template('signup.html', error='Invalid Email Address')
        # * FOR API
    if data['password'] != data['password1']:
        return render_template('signup.html', error='Passwords Does Not Match')
        # * FOR API
    hash = bcrypt.hashpw(data['password'].encode('utf-8'), salt)
    try:
        temp = User(username=data['username'],
                    email=data['email'], password=hash)
        temp.save()
    except NotUniqueError:
        return render_template('signup.html', error='Username / Email Already Registered')
        # * FOR API

    return redirect('/')
    # * FOR API return Response(json.dumps({'Success': 'True'}), mimetype="application/json", status=201)
