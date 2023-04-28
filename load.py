from utils import calculate_model_revenue
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def send_revenue_and_load_database(df1:pd.DataFrame, cur, conn):

    # calcular retorno financeiro
    calculate_model_revenue(df1)

    # Executar uma consulta SQL para verificar se a tabela já existe
    cur.execute("""
        SELECT EXISTS (
            SELECT 1
            FROM   information_schema.tables 
            WHERE  table_name = 'Supermarket_Silver'
        );
    """)

    # Recuperar o resultado da consulta
    table_exists = cur.fetchone()[0]

    # Se a tabela não existir, criar a tabela
    if not table_exists:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Supermarket_Silver (
                store_id INT PRIMARY KEY,
                sales_date DATE,
                store_area INT,
                items_available INT,
                daily_customer_count INT,
                store_sales INT,
                store_cluster INT,
                predict_store_sales FLOAT,
                average_store_sales INT,
                mae_model FLOAT,
                mape_model FLOAT,
                rmse_model FLOAT,
                best_scenario_model FLOAT,
                worst_scenario_model FLOAT
            );
        """)
        conn.commit()
    
    # Popular banco de dados

    # Loop através das linhas do dataframe e inserir cada linha na tabela
    for index, row in df1.iterrows():
        cur.execute("""
            INSERT INTO Supermarket_Silver (store_id, sales_date, store_area, items_available, daily_customer_count, store_sales, store_cluster, predict_store_sales, average_store_sales,
            mae_model, mape_model, rmse_model, best_scenario_model, worst_scenario_model)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, (
            int(row['store_id']),
            row['sales_date'],
            int(row['store_area']),
            int(row['items_available']),
            int(row['daily_customer_count']),
            int(row['store_sales']),
            int(row['store_cluster']),
            float(row['predict_store_sales']),
            int(row['average_store_sales']),
            float(row['mae_model']),
            float(row['mape_model']),
            float(row['rmse_model']),
            float(row['best_scenario_model']),
            float(row['worst_scenario_model'])
        ))

    # Salvar as alterações no banco de dados
    conn.commit()

    # Fechar o cursor e a conexão com o banco de dados
    cur.close()
    conn.close()

    return logging.info("Previsões salvas no banco de dados com sucesso!")