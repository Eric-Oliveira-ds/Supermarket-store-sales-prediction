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
    Calculates the return on investment (ROI) of a model relative to the mean baseline.

    Args:
        df : pandas.DataFrame, a dataframe containing the model's data.

    Returns:
        - "baseline $": the return on the mean baseline in dollars.
        - "model $": the return on the model in dollars.
        - "diff Model/Baseline": the difference between the sum of sales predicted by the model and the baseline, indicating how much more accurately the model predicted sales compared to the baseline.

    This function calculates the ROI of a model by comparing it to a mean baseline. It takes in a pandas DataFrame containing the model's data and returns the return on the baseline, the return on the model, and the difference between the two. The function also prints out the results in a formatted way for easy interpretation. The output will tell whether the model performed better or worse than the baseline, and by how much. 

        """
    # Calcula o retorno do modelo em relação ao baseline de média
    baseline_return = df['average_store_sales'].sum() - df['store_sales'].sum()
    model_return = df['predict_store_sales'].sum() - df['store_sales'].sum()
    diff_model_baseline = (model_return - baseline_return)
    diff_percent = (diff_model_baseline / baseline_return) * 100
    diff_percent_model_store_sales = (model_return / df['store_sales'].sum()) * 100
    diff_percent_baseline_store_sales = (baseline_return / df['store_sales'].sum()) * 100

    # Formata os resultados para exibição
    baseline_return_formatted = f'${baseline_return:,.2f}'
    model_return_formatted = f'${model_return:,.2f}'
    diff_model_baseline_formatted = f'${diff_model_baseline:,.2f}'

    print(f'O baseline de média previu {baseline_return_formatted} em relação as vendas reais.')
    print(f'O modelo previu {model_return_formatted} em relação as vendas reais.')
    print(f'A diferença percentual entre o modelo e as vendas reais são de {abs(diff_percent_model_store_sales):.2f}%')
    print(f'A diferença percentual entre o baseline de média e as vendas reais são de {abs(diff_percent_baseline_store_sales):.2f}%')

    if model_return > baseline_return:
        print(f'O modelo consegue recuperar {diff_model_baseline_formatted} que eram perdidos ao usar a média como previsão de vendas!')
    elif model_return == baseline_return:
        print(f'O modelo obteve o mesmo resultado {diff_model_baseline_formatted} que era previsto ao usar a média como previsão de vendas!')
    else:
        print(f'O modelo obteve resultado pior que usar a média como previsão de vendas {diff_model_baseline_formatted} !')

    return None