from . import bp
from app.erros import bad_request
from app import cross_origin,db
from flask import jsonify,request
from app.authenticate import check_token_dec
from app.models import Cores,Direcao,CoresDirecao

@bp.route('/',methods=['GET','POST'])
@cross_origin()
@check_token_dec
def direcao_():

    try:
        #print(request.method)
        if request.method == 'GET':
            cor = CoresDirecao.query.join(Direcao,Direcao.id_direcao == CoresDirecao.direcao_id) \
                .join(Cores,Cores.id_cores == CoresDirecao.cor_id) \
                .add_columns(CoresDirecao.id_cores_direcao,Cores.nome,Direcao.nome) \
                .all()

            items= []

            for item in cor:
                items.append({
                    "id_cores_direcao":str(item[1]),
                    "cor":str(item[2]),
                    "direcao":str(item[3])
                })

            message = {
                "items":items
            }

            return jsonify(message),200

        data = request.get_json()

        print(data)

        dir_cor = CoresDirecao()
        dir_cor.from_dict(data)

        if request.method == 'POST':
            db.session.add(dir_cor)
            db.session.commit()
            return jsonify({"msg": 'cor inserida com sucesso'}),201

    except Exception as e:
        print(e)
        return bad_request(503,f"""error ao fazer a consulta no metodo {str(request.method)}""")


@bp.route('/deletar',methods=['POST'])
@cross_origin()
@check_token_dec
def delete_direcao():
    try:
        data = request.get_json()

        print(data)

        CoresDirecao.query.filter(CoresDirecao.id_cores_direcao == data['id_cores_direcao']).delete()

#        print(dir_cor)

        db.session.commit()
        return jsonify({"msg": 'cor deletada com sucesso'}),204

    except Exception as e:
        print(e)
        return bad_request(503,f"""error ao fazer delete""")