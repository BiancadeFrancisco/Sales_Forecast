import pandas as pd
import streamlit as st
import pickle as pkl
import datetime as dt
from functions.utility import gerar_df, gerar_store_list, datas
import json
classe = 'PRO'

# LAYOUT PÁGINA #
st.set_page_config(layout="wide")

store_names = gerar_store_list()
store_names = store_names['lojas']

# CONFIG SIDEBAR #

st.sidebar.write("\n\n")
st.sidebar.write("\n\n")

st.sidebar.markdown("SELEÇÃO DO CLIENTE:")
LOJA = st.sidebar.selectbox(
    "Selecione o cliente:", options=store_names
)

# DADOS #

try:
    df = gerar_df(LOJA,classe) #<- corrigir

    st.sidebar.markdown("SELEÇÃO DOS FILTROS:")
    fCategoria = st.sidebar.selectbox(
        "Selecione o produto:", options=df[f"{classe}_CODIGO"].unique() #<- corrigir
    )

    today = dt.datetime.now()
    next_year = today.year + 1
    jan_1 = dt.date(next_year, 1, 1)
    dec_31 = dt.date(next_year, 12, 31)

    fData = st.sidebar.date_input(
        "Selecione a data",
        (jan_1, dt.date(next_year, 1, 7)),
        jan_1,
        dec_31,
        format="YYYY.MM.DD",
    )

    lista_datas = datas(fData[0],fData[1])
    # CONFIG PAGINA #

    st.subheader("PREVISÃO FATURAMENTO POR CATEGORIA DE PRODUTO")

    st.subheader(LOJA)

# MODELO #
    cat_list = [fCategoria for _ in range(len(lista_datas))]
    data_cat = {f'{classe}_CODIGO':cat_list,'VUF_DT':lista_datas} #<- corrigir
    tabela = pd.DataFrame(data=data_cat)


    st.table(tabela)
except:
    st.subheader('A loja não possue base dados', divider='red')

try:
    with open(f"./pages/skmodelos/predict_pipe_{LOJA}_{classe}.pkl", "rb") as MF: #<- corrigir
        model = pkl.load(MF)
except:
    st.subheader('A loja selecionada não possue modelo treinado',divider='red')

if st.sidebar.button("Prever"):

    try:
        tabela['VUF_DT'] = pd.to_datetime(tabela["VUF_DT"])
        previsoes = model.predict(tabela)
        st.success('Prevesão feita com sucesso', icon='✅')
        dados = {'Data':lista_datas,'Valor de venda': list(previsoes)}
        predict_forecasting_df = pd.DataFrame(dados)
        st.line_chart(predict_forecasting_df, x="Data", y="Valor de venda",)
        
        with open(f'./files/best_parameters/{LOJA}_{classe}_parameters.json') as file:
            relatorio = json.load(file)
            
        st.metric("Precisão", value=f'{relatorio["wmape"]["mean"]:.2}')
        st.caption(f'Std :blue[{relatorio["wmape"]["std"]:.2}]')
        
        if relatorio['wmape']['mean'] >= 0.5:
            st.subheader("Modelo com baixa precisão", divider='orange')
        elif relatorio['wmape']['mean'] >= 0.29:
            st.subheader("Modelo com média precisão", divider='orange')
        else:
            st.subheader("Modelo com alta precisão", divider='orange')
    except:
        st.success("Erro ao fazer a previsão")  
