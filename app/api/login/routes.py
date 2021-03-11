from . import bp
from app import cross_origin
from app.models import Usuario,Cadastro
from flask import jsonify,request
from app.authenticate import generate_token,check_token
from app.erros import bad_request

@bp.route('/',methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()

    if data['email'] and data['senha']:
        try:
            user = Usuario.query.filter_by(email=data['email']).first()
        except Exception as e:
            print(e)
            return bad_request(403,'Não possui usuario com esse email')
        check_senha = Cadastro(senha=user.cadastro_usuario[0].senha)
        if user is None or not check_senha.check(data['senha']):

            return bad_request(403,'usuario e/ou senha errado')
        # login_user(user)
        # print(str(user.nome))
        token = generate_token(user)
        return jsonify({
            'message':'usuario {} autenticado com sucesso '.format(str(user.nome)),
            'user': str(user.nome),
            'success':1,
            'token':token
        })
    return bad_request(403,'não foi informado credenciais para login')

@bp.route('/',methods=['GET'])
@cross_origin()
def check_login():
    token_header = request.headers.get('x-access-token')
    if token_header is None:
        return jsonify({
            'message':'Nao foi possivel localizar o token',
            'success':False
        })
    check = check_token(token_header)
    if not check:
        return jsonify({
            'message': 'invalid Token',
            'succes':0
        })
    return jsonify({
        'message':'Token Valido',
        'success':1
    })