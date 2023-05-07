import mlflow
import mlflow.sklearn
import pandas as pd
from utils import mean_absolute_error, mean_absolute_percentage_error, root_mean_squared_error

def predict_and_evaluate(df1:pd.DataFrame, km_model, lr_model, mean_sales)->pd.DataFrame:

    # Prever cluster
    cluster = km_model.predict(df1.drop(['store_id','sales_date','store_sales'], axis=1))
    # Adicionar labels ao conjunto de teste
    df1['store_cluster'] = cluster

    # Separar variáveis independentes e dependente
    X_test = df1.drop(['sales_date','store_sales','daily_customer_count'], axis=1)
    y_pred = lr_model.predict(X_test)

    # adiciona previsão do modelo a base de produção
    df1['predict_store_sales'] = y_pred
    # adiciona previsão de média do baseline a base de teste original
    df1['average_store_sales'] = int(mean_sales)

    # adiciona as métricas técnicas ao dataframe, só teria estas métricas após ter a Target disponível, os dados em produção não teria esta Target store_sales para ser possível metrificar. 
    df1['mae_model'] = df1.apply(lambda x: mean_absolute_error(x['store_sales'], x['predict_store_sales']),axis=1) 
    df1['mape_model'] = df1.apply(lambda x: mean_absolute_percentage_error(x['store_sales'], x['predict_store_sales']),axis=1) 
    df1['rmse_model'] = df1.apply(lambda x: root_mean_squared_error(x['store_sales'], x['predict_store_sales']),axis=1) 
    df1['best_scenario_model'] = df1['predict_store_sales'] + df1['mae_model']
    df1['worst_scenario_model'] = df1['predict_store_sales'] - df1['mae_model']
    # reorganizar colunas
    df1 = df1[['store_id','sales_date','store_area','items_available','daily_customer_count','store_sales','store_cluster','predict_store_sales','average_store_sales','mae_model','mape_model','rmse_model','best_scenario_model','worst_scenario_model']]

    return df1