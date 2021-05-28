from re import M
from . import bp
from app.erros import bad_request
from app import cross_origin,db
from flask import jsonify,request
from app.authenticate import check_token_dec,decode_token
from app.models import Envio,Pedido,Usuario, pedido
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
# @check_token_dec
def envio():

    try:
        def generate_uuid():
            id = uuid.uuid4()
            return id.hex

        data = request.get_json()

        data['codigo_envio'] = generate_uuid()
        data['token'] = generate_uuid()
        data['codigo_pedido'] = data['cod_pedido']
        data['usuario_id'] = data['id_usuario']
        
        # print(data)
        
        qrcode_ = make_qr_code(json.dumps(data))
        
        data['qr_code'] = qrcode_

        envio_ = Envio()
        # print(envio_.__table__.columns)
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

        pedidos = Envio.query.join(Pedido,Pedido.cod_pedido == Envio.codigo_pedido) \
            .filter(Pedido.usuario_id == user_id) \
            .add_columns(Pedido.usuario_id,Envio.codigo_envio,Envio.qr_code,Envio.codigo_pedido,Envio.token) \
            .all()
        
        items= []

        for row in pedidos:
            items.append({
                'id_usuario':row[1],
                'codigo_envio':row[2],
                'qr_code':row[3],
                "codigo_pedido":row[4],
                "token":row[5]
            })

        # print(items)

        message = {
            'items': items
        }

        return jsonify(message),200
    except Exception as e:
        print(e)
        return bad_request(403,'Não foi possivel trazer usuario')


@bp.route('/autenticar',methods=['POST'])
# @cross_origin()
@check_token_dec
def att_status():

    try:

        token = request.headers.get('x-access-token')

        verify_token = decode_token(token)
        user_id = verify_token['id_user']

        data = request.get_json()

        print(data)

        envio_ = Envio.query.filter(Envio.token == data['token']).first()

        user_ = Usuario.query.filter(Usuario.id_usuario == user_id).first()

        pedido_ = Pedido.query.filter(Pedido.cod_pedido == envio_.codigo_pedido).first()

        # new_pedido = Pedido()

        # new_pedido.from_dict(pedido_.to_dict())
        # print(pedido_.to_dict())

        if user_.funcao_id:
            if pedido_.status_id < 4:
                pedido_.status_id += 1
            else:
                pedido_.status_id = 4
        else:
            pedido_.status_id = 4
        
        db.session.commit()
        
        message = {
            'msg':'status do pedido atualizado com sucesso'
        }

        return jsonify(message),201
    except Exception as e:
        print(e)
        return bad_request(403,'Não foi possivel atualizar status ')