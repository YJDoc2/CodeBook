from flask import request, Response, Blueprint, json, session, render_template, redirect, session
from config import blacklist
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required, set_access_cookies, unset_jwt_cookies, get_jwt_identity
from mongoengine.errors import NotUniqueError
from models.User import User
import bcrypt
import re
import datetime

user = Blueprint('user', __name__)

salt = bcrypt.gensalt()
email_rx = re.compile(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')


@user.route('/user/login', methods=['POST'])
def login():
    data = request.form.to_dict()
    if 'username' not in data or 'password' not in data or data['username'].strip() == '' or data['password'].strip() == '':
        # return render_template('login.html', error='Please Fill All Fields')
        return Response(json.dumps({'success': False, 'err': 'Incomplete Fields'}), mimetype="application/json", status=200)
    temp = User.objects(username=data['username'])
    if len(temp) == 0:
        # return render_template('login.html', error='The Email is not registered')
        return Response(json.dumps({'success': False, 'err': 'User Does not Exist'}), mimetype="application/json", status=200)
    temp = temp[0]
    if bcrypt.checkpw(data['password'].encode('utf-8'), temp.password.encode('utf-8')):
        expires = datetime.timedelta(days=1)
        token = create_access_token(
            identity=temp.username, expires_delta=expires)
        resp = Response(json.dumps({'success': True, 'token': token,
                                    'link': '/dashboard'}), mimetype="application/json", status=200)
        set_access_cookies(resp, token)
        return resp
        # return redirect('/dashboard')
    else:
        # return render_template('login.html', error='Password Does not match')
        return Response(json.dumps({'success': False, 'err': 'Password does not match'}), mimetype="application/json", status=200)


@user.route('/user/signup', methods=['POST'])
def signup():
    data = request.form.to_dict()

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

    return redirect('/login')
    # * FOR API return Response(json.dumps({'Success': 'True'}), mimetype="application/json", status=201)


@user.route('/api/find/<string:name>', methods=['GET'])
@jwt_required
def find(name):
    pattern = re.compile(name, re.IGNORECASE)
    ret = User.objects(username=pattern)
    ret = [user.to_mongo() for user in ret]
    user = User.objects(username=get_jwt_identity())[0].to_mongo()
    ret = [u for u in ret if (u['_id']
                              not in user['following'] and u['username'] != user['username'])]
    for user in ret:
        del user['_id']
        del user['password']
        del user['posts']
        del user['following']
        del user['followers']
    return Response(json.dumps({'success': True, 'users': ret}), mimetype="application/json", status=201)


@user.route('/api/follow/<string:name>')
@jwt_required
def follow(name):
    u1 = User.objects(username=get_jwt_identity())[0].to_mongo()
    u2 = User.objects(username=name)[0].to_mongo()
    User.objects(username=get_jwt_identity()).update_one(
        push__following=u2['_id'])
    User.objects(username=name).update_one(push__followers=u1['_id'])
    return Response(json.dumps({'success': True}), mimetype="application/json", status=201)


@user.route('/user/logout', methods=['GET'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    resp = redirect('/')
    unset_jwt_cookies(resp)
    return resp
