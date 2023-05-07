import pandas as pd
import numpy as np
import psycopg2
import os
import mlflow
import mlflow.sklearn
from dotenv import load_dotenv
from flask import Flask, request, jsonify

from extract import extract_database
from transform import predict_and_evaluate
from load import send_revenue_and_load_database

import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Variáveis de ambiente
dotenv_path = r"C:\Users\erico\Documents\projeto-regressao\Supermarket-store-sales-prediction\.env\.env"
load_dotenv(dotenv_path)

logging.info("Conectando-se ao PostgreSQL")
# Conectar ao banco de dados
conn = psycopg2.connect(host="localhost",database="Supermarket",user="postgres",password=os.environ.get('PG_PASSWORD'))
# Abrir um cursor para executar consultas
cur = conn.cursor()
cur.execute("ROLLBACK")

logging.info("Conectando-se ao servidor Mlflow e carregando modelos registrados")
# MLFLOW
mlflow.set_tracking_uri('http://127.0.0.1:5000')
# Kmeans
logged_model_cluster = 'runs:/9bc39f393f054e67a5902f1e535e252f/Kmeans_12'
km_model = mlflow.pyfunc.load_model(logged_model_cluster)
# Regressão Linear 
logged_model_sales = 'runs:/0951c733113245be85b36d06bf882950/linear_regression_opt_roi'
lr_model = mlflow.pyfunc.load_model(logged_model_sales)

# API
app = Flask(__name__)
@app.route('/')
def home():
    return 'Esta é uma API Flask instânciando um end-point'

@app.route('/predict', methods=['GET'])
def predict():
    logging.info("Extraindo base de dados do banco de dados e calculando a média das vendas dos últimos 30 dias")
    # Extração
    df1, mean_sales = extract_database(cur=cur, conn=conn)
    logging.info("Transformando base de dados para adequar-se aos modelos de machine learning e aplicando previsões e avaliações")
    # Transformação e previsão
    df1 = predict_and_evaluate(df1=df1, km_model=km_model, lr_model=lr_model, mean_sales=mean_sales)
    logging.info("Carregando base de dados com as vendas previstas para o banco de dados")
    # Carga
    send_revenue_and_load_database(df1=df1, cur=cur, conn=conn)

    return jsonify(df1.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(port=5500, debug=True)