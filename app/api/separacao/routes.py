from . import bp
from app.erros import bad_request
from app import cross_origin,db
from flask import jsonify,request
from app.models import Cores,CoresDirecao,Direcao

import requests
import json
from PIL import Image
import numpy as np
import base64
from io import BytesIO

IMG_SIZE = 128

def convert_image(image_64):

    byte_data = base64.b64decode(image_64)
    image_data = BytesIO(byte_data)

    img_array = Image.open(image_data)
    new_array = img_array.resize((IMG_SIZE, IMG_SIZE))

    new_array = np.expand_dims(new_array,axis=0)

    img_new_array = new_array / 255

    data = json.dumps(
        {"signature_name": "serving_default", "instances": img_new_array.tolist()})
    
    return data

def rotacao_motor(direcao):
    try:
        get_direcao = Direcao.query.filter_by(id_direcao=direcao).first()
        
        rotacao_direita = ['direita'] # recebera a matriz correspondete ao movimento da direita
        rotacao_esquerda = ['esquerda']# recebera a matriz correspondete ao movimento da esquerda

        return rotacao_direita if get_direcao.nome == 'right' else rotacao_esquerda
    except:
        return bad_request(500,'não foi possivel trazer a direção do motor')

@bp.route('/',methods=['POST'])
def get_predict():
    try:
        data = request.get_json()

        headers = {"content-type":"application/json"}

        img = convert_image(data['image'])

        response = requests.post("http://localhost:5000/predict",data=img,headers=headers) # request ao tensorflow serving 

        predict_class = response.json()['predict']

        cor = Cores.query.filter_by(nome=predict_class).first()
        direcao = CoresDirecao.query.filter_by(cor_id = cor.id_cores).first()

        mover_motor = rotacao_motor(direcao.direcao_id)

        return jsonify({
            'predict_class':predict_class,
            'direcao':mover_motor
        })
        
    except:
        return bad_request(500,'não foi possivel fazer a previsão da cor.')