import pandas as pd
import psycopg2

def extract_database(cur,conn):

    # Consultar o banco de dados e obter média das store_sales dos últimos 30 dias excluindo os últimos 30 dias que serão previstos pelo modelo de regressão linear
    query = """ SELECT AVG(store_sales) AS avg_sales
                FROM Supermarket_Gold
                WHERE sales_date >= NOW() - INTERVAL '30 DAY'
                AND store_id NOT IN (
                    SELECT store_id
                    FROM Supermarket_Gold
                    ORDER BY sales_date DESC
                    LIMIT 30
                );
            """

    cur.execute(query)
    mean_sales_30 = cur.fetchone()[0]
    # Consultar o banco de dados e criar o DataFrame pandas. Últimos 30 store_id (30 dias) 
    query = """ SELECT * FROM Supermarket_Gold 
                ORDER BY store_id 
                DESC LIMIT 30; 
            """
    df1 = pd.read_sql_query(query, conn)

    return df1, mean_sales_30