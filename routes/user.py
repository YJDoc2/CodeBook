from flask import request, Response, Blueprint, json, session, render_template
import bcrypt
from models.User import User

user = Blueprint('user', __name__)

salt = bcrypt.gensalt()


@user.route('/user/login', methods=['POST'])
def login():
    data = request.form.to_dict()
    if 'email' not in data or 'password' not in data:
        return Response(json.dumps({'Success': 'False', 'error': 'Incomplete Fields'}), mimetype="application/json", status=404)
    temp = User.objects(email=data['email'])
    if len(temp) == 0:
        return Response(json.dumps({'Success': 'False', 'Error': 'User Does not Exist'}), mimetype="application/json", status=404)
    temp = temp[0]
    if bcrypt.checkpw(data['password'].encode('utf-8'), temp.password.encode('utf-8')):
        return Response(json.dumps({'Success': 'True'}), mimetype="application/json", status=200)
    else:
        return Response(json.dumps({'Error': 'Password does not match'}), mimetype="application/json", status=400)


@user.route('/user/signup', methods=['POST'])
def signup():
    data = request.form.to_dict()
    if 'email' not in data or 'password' not in data or 'username' not in data:
        return Response(json.dumps({'Success': 'False', 'error': 'Incomplete Fields'}), mimetype="application/json", status=404)
    hash = bcrypt.hashpw(data['password'].encode('utf-8'), salt)
    temp = User(username=data['username'], email=data['email'], password=hash)
    temp.save()
    return Response(json.dumps({'Success': 'True'}), mimetype="application/json", status=201)
