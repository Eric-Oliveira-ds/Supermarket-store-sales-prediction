import pandas as pd
import numpy as np

# Utils
def mean_absolute_percentage_error(y_true, yhat):
    return np.mean(np.abs((y_true - yhat) / y_true))

def mean_absolute_error(y_true, yhat):
    return np.mean(np.abs(y_true - yhat))

def root_mean_squared_error(y_true, yhat):
    return np.sqrt(np.mean(np.square(y_true - yhat)))


def calculate_model_revenue(df:pd.DataFrame):
    """
        Calcula o retorno do investimento (ROI) de um modelo em relação ao baseline de média.

        Args:
            df : pandas.DataFrame, um dataframe contendo os dados do modelo.

        Returns:
            - "Baseline $": o retorno do baseline de média em dólares
            - "Model $": o retorno do modelo em dólares
            - "Diff Model/Baseline": a diferença entre a soma de vendas prevista pelo modelo e pelo baseline, diz o quanto o modelo acertou a mais que o baseline em termos de vendas
        """
    # Calcula o retorno do modelo em relação ao baseline de média
    baseline_return = df['average_store_sales'].sum() - df['store_sales'].sum()
    model_return = df['predict_store_sales'].sum() - df['store_sales'].sum()
    diff_model_baseline = (model_return - baseline_return)
    
    # Formata os resultados para exibição
    baseline_return_formatted = f'${baseline_return:,.2f}'
    model_return_formatted = f'${model_return:,.2f}'
    diff_model_baseline_formatted = f'${diff_model_baseline:,.2f}'

    print(f'O valor do retorno do baseline de média é de {baseline_return_formatted}')
    print(f'O valor do retorno do modelo é de {model_return_formatted}')
    print(f'A diferença entre o modelo e o baseline de média é de {diff_model_baseline_formatted}')
    print(f'O modelo consegue recuperar {diff_model_baseline_formatted} que eram perdidos ao usar a média como previsão de vendas!')
    
    return None