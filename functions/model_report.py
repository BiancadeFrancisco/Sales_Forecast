from sklearn.model_selection import train_test_split
import pickle as pkl
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_absolute_percentage_error
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, GridSearchCV, KFold
import json
import functions.utility as ut
import time
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder

def machine_traing_project(loja:str, parametro:str):
    start = time.time()
    with open(f"./tabelas_casting/{loja}_{parametro}.pkl",'rb') as fi:
        df = pkl.load(fi)

    y = df['VUF_VLRBRUTOVENDA']
    X = df.drop(columns=['VUF_VLRBRUTOVENDA'], axis=1)

    print(f'Tabela {loja}_{parametro} importada e fracionada com sucesso')


    pipeline = make_column_transformer(
    (ut.date_transform_pipe,['VUF_DT']),
    (OneHotEncoder(),[f'{parametro}_CODIGO'])
    )

    grid_pipe = Pipeline(
    steps=[
        ('pipeline', pipeline)
        ]
    )

    grid_pipe.fit(X)
    print(X.shape)
    X_transformed=grid_pipe.fit_transform(X)
    print(X_transformed.shape)

    # Realizando o gridsearch

    print(f"Executando o grid search para {loja}_{parametro}")
    random_grid = {'n_estimators': ut.n_estimators,
                'max_depth': ut.max_depth,
                'min_samples_split': ut.min_samples_split,
                'min_samples_leaf': ut.min_samples_leaf,
                'bootstrap': ut.bootstrap}
    kfold = KFold(n_splits=5, shuffle=True, random_state=42)
    grid = GridSearchCV(
        estimator=RandomForestRegressor(),
        param_grid=random_grid, cv=kfold,
        n_jobs=-1,
        verbose = 10
        )
    grid.fit(X=X_transformed, y=y)
    best_parameters = grid.best_params_
    print(f'Melhores parâmetros: {best_parameters}')

    # Realizando o cross validation com o modelo tunado

    print(f'Criando o predict_pipe tunado para o {loja}_{parametro}')


    predict_pipe = Pipeline(
        steps=[
            ('pipeline', pipeline),
            ('model',RandomForestRegressor(
                n_estimators=best_parameters['n_estimators'],
                min_samples_split=best_parameters['min_samples_split'],
                min_samples_leaf=best_parameters['min_samples_leaf'],
                max_depth=best_parameters['max_depth'],
                bootstrap=best_parameters['bootstrap'],
                random_state=42
                                        ))
            ]
        )

    # validando o modelo usando 5-fold cross-validation

    print(f'Realizando o cross validation para {loja}_{parametro}')
    Kfold = KFold(n_splits=10, shuffle=True, random_state=42)
    scores = cross_val_score(predict_pipe, X=X, y=y, cv=Kfold)

    Scores = pd.DataFrame({'Scores':scores})
    describes = Scores.describe()
    describes = describes.to_dict()


    # Métricas de precisão da regressão
    print(f'Criando as métricas do predict_pipe para {loja}_{parametro}')
    mae_list=[]
    mse_list=[]
    wmape_list=[]
    r2_list=[]
    mape_list=[]

    for i in range(12, 62, 10):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=i)
        predict_pipe.fit(X_train,y_train)
        y_pred = predict_pipe.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        wmp = ut.wmape(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)

        mae_list.append(mae)
        mse_list.append(mse)
        wmape_list.append(wmp)
        r2_list.append(r2)
        mape_list.append(mape)


    end = time.time()
    print(f'A operação demorou {end - start} para processar')
    tempo = (end - start)/60
    ## Relatório diário
    print(f'Gerando o relatório do {loja}_{parametro}')


    document = {
                'loja':loja,
                'parametro':parametro,
                'parameters':best_parameters,
                'describes':describes,
                'mae':{
                    'mean':ut.mean_list(mae_list),
                    'std':ut.std_list(mae_list)},
                'mse':{
                    'mean':ut.mean_list(mse_list),
                    'std':ut.std_list(mse_list)},
                'r-quadrado':{
                    'mean':ut.mean_list(r2_list),
                    'std':ut.std_list(r2_list)},
                'wmape':{
                    'mean':ut.mean_list(wmape_list),
                    'std':ut.std_list(wmape_list)},
                'mape':{
                    'mean':ut.mean_list(mape_list),
                    'std':ut.std_list(mape_list)},
                'time':tempo}

    time.sleep(3)
    print(f'salvando os hiperparâmetros do predict_model {loja}_{parametro}')
    with open(f'./files/best_parameters/{loja}_{parametro}_parameters.json', 'w') as f:
        json.dump(document, f)

    time.sleep(3)
    print(f'Salvando o predict_model treinado para {loja}_{parametro}\n \n \n')
    with open(f'./pages/skmodelos/predict_pipe_{loja}_{parametro}.pkl','wb') as f:
        pkl.dump(predict_pipe, f)

    time.sleep(3)








