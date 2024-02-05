import numpy as np
import pandas as pd
from sklearn.preprocessing import FunctionTransformer   
import json
import datetime as dt


def std_list(lista:list):
    mean = sum(lista) / len(lista) 
    variance = sum([((x - mean) ** 2) for x in lista]) / len(lista) 
    return variance ** 0.5

def mean_list(lista:list):
    return sum(lista) / len(lista) # salvar essa função 

def wmape(y_true, y_pred):
    return np.abs(y_true - y_pred).sum() / np.abs(y_true).sum()

def date_transform(df:pd.DataFrame) -> pd.DataFrame:
    df['Week'] = df['VUF_DT'].dt.isocalendar().week.astype('int64')
    df['Month'] = df['VUF_DT'].dt.month.astype('int64')
    df['WeekDay'] = df['VUF_DT'].dt.day_of_week
    df.drop(columns=['VUF_DT'], axis=1, inplace=True)
    return df
date_transform_pipe = FunctionTransformer(date_transform)

parametros = ['CAT']

lojas = [
           'DB063',
           'DB069',
           'DB088',
           'DB092',
           'DB101',
           'DB108',
           'DB109',
           'DB113'
        ] # IDs das lojas que serão utilizadas

## Lista de hiperparâmetros a ser utilizados 
n_estimators = [40, 60]
max_depth = [10]
max_depth.append(None)
min_samples_split = [2, 5]
min_samples_leaf = [1, 2]
bootstrap = [True, False]

def gerar_df(LOJA,CLASS):
    caminho_arquivo = f".\\tabelas_casting\\{LOJA}_{CLASS}.pkl"
    return pd.read_pickle(caminho_arquivo)

def gerar_store_list():
    with open('.\\tabelas_casting\\lojas.json', 'r') as f:
        names = json.load(f)
    return names

def datas(data_inicial,data_final):
    num_of_dates = data_final - data_inicial
    date_list = [data_inicial + dt.timedelta(days=x) for x in range(num_of_dates.days)]
    return date_list

def report(loja:str,
           parametro:str,
           best_parameters:dict,
           describes:dict,
           mae_mean,
           mae_std,
           mse_mean,
           mse_std,
           rqua_mean,
           rqua_std,
           wmape_mean,
           wmape_std,
           mape_mean,
           mape_std,
           tempo):
    with open(f'.\\files\\reports\\relatório_de_{loja}_{parametro}_{dt.datetime.today().strftime("%d-%m-%Y")}.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(f'Atualização do modelo preditivo de vendas\n \n \
        Loja: {loja} \n\
        Parâmetro: {parametro} \n')
        arquivo.write(f'Parâmetros mais efetivos: \n \n \
        n_estimators = {best_parameters["n_estimators"]}\n \
        min_samples_split = {best_parameters["min_samples_split"]} \n \
        min_samples_leaf = {best_parameters["min_samples_leaf"]} \n \
        max_depth = {best_parameters["max_depth"]} \n \
        bootstrap = {best_parameters["bootstrap"]} \n \n\
        Estatísticas descritivas das métricas dos folders: \n \
                    {describes}\n \n \
        As métricas levantadas foram: \n \
        mae: {"média",mae_mean,"/ desvio padrão", mae_std}, \n \
        mse: {"média",mse_mean,"/ desvio padrão", mse_std} \n\
        r-quadrado: {"média",rqua_mean,"/ desvio padrão", rqua_std} \n\
        wmape: {"média",wmape_mean,"/ desvio padrão", wmape_std} \n \
        mape: {"média",mape_mean, "/ desvio padrão",mape_std}\n \n \
        tempo de processamento: {tempo} minutos')
        
def get_report(loja:str, classe:str):
    with open(f'.\\files\\best_parameters\\{loja}_{classe}_parameter.json') as file:
        report = json.load(file)
    return report
