import re
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

@bp.route('/',methods=['POST'])
@cross_origin()
# @check_token_dec
def get_predict():
    try:
        
        data = request.get_json()

        # print(request)
        # print(request.data)

        data_receveid = json.loads(request.data)
        # print(data_receveid)
        headers = {"content-type":"application/json"}

        img = convert_image(data_receveid['image'])

        response = requests.post("http://34.72.212.91:9000/v1/models/IA_PI-VII:predict",data=img,headers=headers) # request ao tensorflow serving 

        predictions = response.json()['predictions']

        labels = {0: 'blue', 1: 'green', 2: 'red', 3: 'yellow'}

        predict_class = np.argmax(predictions[0])

        predict_cor = labels[predict_class]
        
        cor = Cores.query.filter_by(nome=predict_cor).first()

        print(cor)
        direcao = CoresDirecao.query.filter_by(cor_id = cor.id_cores).first()
        print(direcao)

        mover_motor = Direcao.query.filter_by(id_direcao=direcao.direcao_id).first()
        print(mover_motor)

        return jsonify({
            'predict_class': predict_cor,
            'direcao': str(mover_motor.id_direcao)
        })

    except Exception as e:
        print(e)
        return bad_request(500,'não foi possivel fazer a previsão da cor.')
