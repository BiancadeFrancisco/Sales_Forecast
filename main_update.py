from functions.model_report import machine_traing_project
from functions.utility import lojas, parametros, report
from tqdm import tqdm
import json

for loja in tqdm(lojas):
    for parametro in tqdm(parametros):
        try:
            print(f'Loja {loja}, sendo treinada para o parâmetro {parametro}')
            machine_traing_project(loja, parametro)
            with open(f'.\\files\\best_parameters\\{loja}_{parametro}_parameters.json') as file:
                document = json.load(file)
            report(document['loja'],
                   document['parametro'],
                   document['parameters'],
                   document['describes']['Scores'],
                   document['mae']['mean'],
                   document['mae']['std'],
                   document['mse']['mean'],
                   document['mse']['std'],
                   document['r-quadrado']['mean'],
                   document['r-quadrado']['std'],
                   document['wmape']['mean'],
                   document['wmape']['std'],
                   document['mape']['mean'],
                   document['mape']['std'],
                   document['time']
                   )
        except Exception as e:
            print(f'Problema ao processar o campo {loja} com {parametro}: {e}')
             
    