from . import bp
from app.erros import bad_request
from app import cross_origin
from flask import jsonify,request
from app.models import Cores,CoresDirecao,Direcao
from io import BytesIO
from app.authenticate import check_token_dec
from PIL import Image

import requests
import json
import numpy as np
import base64

IMG_SIZE_WIDTH = 128
IMG_SIZE_HEIGHT = 128

def convert_image(image_64:str) -> str:
    try:

        byte_data = base64.b64decode(image_64)
        image_data = BytesIO(byte_data)

        img_array = Image.open(image_data)
        new_array = img_array.resize((IMG_SIZE_WIDTH, IMG_SIZE_HEIGHT))

        new_array = np.expand_dims(new_array,axis=0)

        img_new_array = new_array / 255

        data = json.dumps(
            {"signature_name": "serving_default", "instances": img_new_array.tolist()})
        
        return data
    except Exception as e:
        raise e

def rotacao_motor(direcao:int) -> list:
    try:
        get_direcao = Direcao.query.filter_by(id_direcao=direcao).first()
        
        rotacao_direita = ['direita'] # recebera a matriz correspondete ao movimento da direita
        rotacao_esquerda = ['esquerda']# recebera a matriz correspondete ao movimento da esquerda

        return rotacao_direita if get_direcao.nome == 'right' else rotacao_esquerda
    except Exception as e:
        raise e
        # return bad_request(500,'não foi possivel trazer a direção do motor')

@bp.route('/',methods=['POST'])
@cross_origin()
@check_token_dec
def get_predict():
    try:
        data = request.get_json()

        headers = {"content-type":"application/json"}

        img = convert_image(data['image'])

        response = requests.post("http://10.128.0.2:9000/v1/models/IA_PI-VII:predict",data=img,headers=headers) # request ao tensorflow serving 

        predict_class = response.json()['predict']

        cor = Cores.query.filter_by(nome=predict_class).first()
        direcao = CoresDirecao.query.filter_by(cor_id = cor.id_cores).first()

        mover_motor = rotacao_motor(direcao.direcao_id)

        return jsonify({
            'predict_class':predict_class,
            'direcao':mover_motor
        })
        
    except Exception as e:
        return bad_request(500,'não foi possivel fazer a previsão da cor.')