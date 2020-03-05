from flask import request, Response, Blueprint, json, session, render_template

from models.Post import Post
from config.languages import C, CPP, CPP14, JAVA, NODE, PYTHON2, PYTHON3
post = Blueprint('post', __name__)


@post.route('/post', methods=['POST'])
def postChallenge():
    data = request.form.to_dict()

    # print(C.invalid)
    print(data['code'])
    if (data['code'] in C.invalid or data['code'] in CPP.invalid or data['code'] in CPP14.invalid or data['code'] in JAVA.invalid or data['code'] in PYTHON2.invalid or data['code'] in PYTHON3.invalid):

        return Response(json.dumps({'Success': 'False'}), mimetype="application/json", status=201)

    else:

        temp = Post(originalPostBy=data['originalPostBy'],
                    question=data['question'], code=data['code'])
        # testcases=data['testcases'], outputs=data['outputs'])
        temp.save()
        return Response(json.dumps({'Success': 'True'}), mimetype="application/json", status=201)
