from . import bp
from app import cross_origin
from app.models import Pedido,Produto,ProdutosPedidos
from flask import jsonify,request
from app.authenticate import generate_token,check_token_dec,decode_token
from app.erros import bad_request

@bp.route('/',methods=['GET'])
@check_token_dec
def get_pedidos():
    try:
        
        token = request.headers.get('x-access-token')

        verify_token = decode_token(token)
        user_id = verify_token['id_user']

        pedidos = Pedido.query.join(ProdutosPedidos,ProdutosPedidos.pedido_id == Pedido.cod_pedido) \
            .join(Produto,Produto.id_produto == ProdutosPedidos.produto_id) \
            .add_columns(Pedido.cod_pedido,Pedido.data,Pedido.status,Pedido.usuario_id,Produto.descricao)\
            .filter(Pedido.usuario_id == user_id) \
            .all()

        items = []

        for row in pedidos:
            items.append({
                'codigo_pedido':row[1],
                'data': str(row[2]),
                'status': str(row[3]),
                'descricao':row[5]
            })
        
        message = {
            'items': items
        }
        return jsonify(message),200
    except Exception as e :
        print(e)