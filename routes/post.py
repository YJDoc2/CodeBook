from flask import request, Response, Blueprint, json, session, render_template, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.User import User
from models.Post import Post
from config.lang_config import langs
from util.compile import compile_and_run_code
import re

post = Blueprint('post', __name__)

ename = re.compile(r'File \./temp/*\.py$')


@post.route('/api/post', methods=['POST'])
@jwt_required
def postChallenge():
    data = request.form.to_dict()
    ops = []
    qtype = data['type']
    data['testcases'] = json.loads(data['testcases'])
    lang = langs[data['lang']]
    user = get_jwt_identity()
    if any(bad in data['code'] for bad in lang.invalid):
        ret = ''
        for i in lang.invalid:
            ret += i
        return Response(json.dumps({'success': False, 'err': 'Unsupported functions used.\nCannot use These Functions : '+ret}), mimetype="application/json", status=200)
    else:
        for i, tc in enumerate(data['testcases']):
            op = compile_and_run_code(lang, data['code'], tc)
            if not op['success']:
                if op['timeout']:
                    return Response(json.dumps({'success': False, 'err': 'Time out occured for Case #'+str(i+1)}), mimetype="application/json", status=200)
                else:
                    return Response(json.dumps({'success': False, 'err': 'Error in TestCase #'+str(i+1)+op['err']}), mimetype="application/json", status=200)
            else:
                ops.append(op['output'])

    # return Response(json.dumps({'Success': 'True', 'op': ops}), mimetype="application/json", status=200)
    temp = Post(originalPostBy=user, title=data['title'], qtype=qtype,
                description=data['description'], code=data['code'], testcases=data['testcases'], outputs=ops)
    temp.save()
    User.objects(username=get_jwt_identity()).update_one(push__posts=temp.ID)
    return Response(json.dumps({'success': True, 'link': '/dashboard'}), mimetype="application/json", status=201)


@post.route('/mypost/<uuid:id>', methods=['GET'])
@jwt_required
def mypost(id):
    user = User.objects(username=get_jwt_identity())[0].to_mongo()
    if id not in user['posts']:
        return redirect('/dashboard')

    post = Post.objects(ID=id)[0].to_mongo()
    return render_template('viewpost.html', logged_in=True, post=post)


@post.route('/solve/<uuid:id>', methods=['GET'])
@jwt_required
def solve(id):
    user = User.objects(username=get_jwt_identity())[0].to_mongo()
    if id in user['posts']:
        return redirect('/dashboard')
    try:
        post = Post.objects(ID=id)[0].to_mongo()
        return render_template('solve.html', langs=langs, logged_in=True, post=post)
    except:
        return redirect('/dashboard')


@post.route('/submit/<uuid:id>', methods=['POST'])
@jwt_required
def submit(id):
    data = request.form.to_dict()
    ops = []
    lang = langs[data['lang']]
    user = get_jwt_identity()
    try:
        post = Post.objects(ID=id)[0].to_mongo()
        if any(bad in data['code'] for bad in lang.invalid):
            ret = ''
            for i in lang.invalid:
                ret += i
            return Response(json.dumps({'success': False, 'err': 'Unsupported functions used.\nCannot use These Functions : '+ret}), mimetype="application/json", status=200)
        else:
            for i, tc in enumerate(post['testcases']):
                op = compile_and_run_code(lang, data['code'], tc)
                if not op['success']:
                    if op['timeout']:
                        return Response(json.dumps({'success': False, 'err': 'Time out occured for Case #'+str(i+1)}), mimetype="application/json", status=200)
                    else:
                        return Response(json.dumps({'success': False, 'err': 'Error in TestCase #'+str(i+1)+op['err']}), mimetype="application/json", status=200)
                else:
                    ops.append(op['output'])

            for i, op in enumerate(ops):
                if op == post['outputs'][i]:
                    continue
                else:
                    return Response(json.dumps({'success': False, 'err': 'Error in TestCase #'+str(i+1)+'\nExpected : '+post['outputs'][i]+'\nGot : '+op}), mimetype="application/json", status=200)
            User.objects(username=get_jwt_identity()
                         ).update_one(push__posts=post['_id'])
            return Response(json.dumps({'success': True, 'link': '/dashboard'}), mimetype="application/json", status=201)
    except:
        return Response(json.dumps({'Success': False, 'redirect': '/'}), mimetype="application/json", status=200)


@post.route('/solution/<uuid:id>', methods=['GET'])
@jwt_required
def solution(id):
    user = User.objects(username=get_jwt_identity())[0].to_mongo()
    try:
        post = Post.objects(ID=id)[0].to_mongo()
        if id not in user['posts']:
            User.objects(username=get_jwt_identity()).update_one(
                push__posts=post['_id'])
        return render_template('solution.html', logged_in=True, post=post)
    except:
        return redirect('/')
