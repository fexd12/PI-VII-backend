from . import bp
from app.erros import bad_request
from app import cross_origin,db
from flask import jsonify,request
from app.authenticate import check_token_dec,decode_token
from app.models import Usuario,Cadastro,Funcao,Envio
import json,qrcode,uuid,base64,io

def make_qr_code(data):
    qrcode_ = qrcode.QRCode()

    qrcode_.add_data(data)
    qrcode_.make(fit=True)

    img = qrcode_.make_image()

    img_bytes = io.BytesIO()

    img.save(img_bytes)

    str =  base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    return str

@bp.route('/',methods=['POST'])
@cross_origin()
@check_token_dec
def envio():

    try:

        data = request.get_json()

        data['codigo_envio'] = uuid.uuid4()
        data['token'] = uuid.uuid4()

        data['usuario_id'] = data['id_usuario']
        
        qrcode_ = make_qr_code(data)
        
        data['qr_code'] = qrcode_

        envio_ = Envio()
        envio_.from_dict(data)
        
        db.session.add(envio_)
        db.session.commit()

        message = {
            'message':'Envio criado'
        }

        return jsonify(message),201
    except Exception as e:
        print(e)
        return bad_request(403,'Não foi possivel trazer usuario')

@bp.route('/qrcode',methods=['GET'])
@cross_origin()
@check_token_dec
def qr_code():

    try:

        token = request.headers.get('x-access-token')

        verify_token = decode_token(token)
        user_id = verify_token['id_user']

        users = Envio.query.join(Usuario,Envio.usuario_id == Usuario.id_usuario) \
            .filter(Usuario.ativo == 'S',Usuario.id_usuario == user_id) \
            .add_columns(Usuario.id_usuario,Usuario.nome,Envio.codigo_envio,Envio.qr_code) \
            .all()
        
        items= []

        for row in users:
            items.append({
                'id_usuario':row[1],
                'nome':row[2],
                'codigo_envio':row[3],
                'qr_code':row[4],
            })

        print(items)

        message = {
            'items': items
        }

        return jsonify(message),200
    except Exception as e:
        print(e)
        return bad_request(403,'Não foi possivel trazer usuario')
