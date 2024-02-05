import pandas as pd
import streamlit as st
import pickle as pkl
import webbrowser
from PIL import Image

# Page Config

img = Image.open("./img/logo.png")
st.set_page_config(page_title="Solução Casting", page_icon=img, layout="wide")

# inicio
st.image("./img/logo_completo.png")
st.write("\n\n")

# site empresa #

btn = st.button("Acesse o site oficial")

if btn:
    webbrowser.open_new_tab("https://www.cstng.com/")

# descrição projeto  #

st.write("\n\n")
st.write("\n\n")
st.write("**Previsão de Faturamento**")
st.write("\n\n")
st.caption(
    "   A previsão de faturamento dessa aplicação é baseada através da análise de dados históricos de vendas, segmentada por clientes. Sendo observado padrões,\
    interações e tendências de consumo de cada cliente. Para alcançar uma previsão de forma detalhada, o algoritmo de aprendizado de máquina utilizado nessa\
    aplicação foi treinado para analisar e prever as vendas de cada cliente, levando em consideração três parâmetros: Loja que é realizado a venda, Produto que\
    foi vendido e Categoria do produto vendido." 
)
st.write("\n\n")
st.write("**Descrição do aplicativo**")
st.write("\n\n")
st.caption("Ao lado, é possível selecionar  a opção do parâmetro que gostaria de fazer a previsão. Dessa forma, o aplicativo\
    direcionará para a página de previsão do parâmetro, local onde é possível selecionar:  o cliente a ser analisado, o parâmetro a ser previsto e o período de\
    previsão. Após os dados serem selecionados, a previsão é realizada ao clicar no botão: Prever. \n   E então, a previsão é realizada e detalhada no centro da página\
    através da visualização de um gráfico de linhas, seguido pelo destaque da performance do modelo de machine learning, treinado para aqueles parâmetros . O valor \
    da métrica do modelo, que é destacada logo abaixo do gráfico de previsão irá variar de 0 a 1,  sendo quanto mais próximo o valor for de 0, melhor é a performance\
    do modelo.")
st.write("\n\n")
st.caption("O uso desse aplicativo de aprendizado de máquina para previsão de faturamento permite que a empresa economize tempo e recursos, sendo possível tomar\
    medidas proativas baseada em dados e informações precisos para, alcançar metas de vendas, monitorar estoques de produtos, etc.")

