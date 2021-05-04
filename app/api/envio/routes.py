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

        data= request.get_json()

        data['codigo_envio'] = uuid.uuid4()
        data['usuario_id'] = data['id_usuario']

        envio_ = Envio()
        envio_.from_dict(data)
        
        db.session.add(envio_)
        db.session.commit()

        message = {
            'message':'Envio criado'
        }

        return jsonify(message),200
    except Exception as e:
        print(e)
        return bad_request(403,'Não foi possivel trazer usuario')

@bp.route('/qrcode',methods=['POST'])
@cross_origin()
@check_token_dec
def qr_code():

    try:

        data = request.get_json()

        dados_envio = Envio.query.filter_by(codigo_envio=data['id_envio']).first()
        print(dados_envio)
        qrcode_ = make_qr_code(dados_envio.to_dict())

        message = {
            'message':'qrcode criado',
            'img': [qrcode_]
        }

        return jsonify(message),200
    except Exception as e:
        print(e)
        return bad_request(403,'Não foi possivel trazer usuario')
