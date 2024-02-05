# Trend Sales (TS)

Serviço de machine learning focado no calculo de faturamento dos clientes referentes a diferentes parâmetros dos clientes da empresa.

## Modo de uso
O serviço apresenta três páginas as quais depositam as máquinas preditivas voltadas a aspectos específicos dos clientes. Esses aspectos seriam as lojas, produto e categorias de produtos. Ao selecionar uma página, o usuário configura os filtros referentes ao cliente e ao detalhamento necessário para previsão. 

## Módulos do serviço

O serviço possui dois arquivos executáveis. Um desenvolvido para para o treinamento e registro dos modelos e outro voltado a produção do modelo e operação pelo cliente. 

### Módulo de treinamento 
O módulo de treinamento coleta os dados registrados no repositório ou na base dados e começa a fazer o treinamento e atualização da dos modelos para cada um dos parâmetros de 
cada uma das lojas. Primeiro realiza o gridsearch para identificação dos conjuntos de hiperparâmetros ideias, realizando em seguia um cross validation para tirar as métricas desses parâmetros. Os modelos treinados então são salvos em um pasta específica. Os detalhes dos modelos são armazenados em formato de dicionários e um relatório quanto as características do modelo e do treinamento são salvos em uma outra pasta.
```
python main_update.py 
```
### Módulo de produção
O segundo módulo faz umas capturas dos modelos treinados e os disponibiliza nas telas aplicadas para execução do modelo em produção.
```
streamlit run 1_◻️_INICIO.py
```

## Organização do serviço
- 📁 Trend Sales
    - 📁 .streamlit -> configurações das páginas
        - 📄 config.toml -> configurações do streamlit
    - 📁 files -> registros de treinamento do modelo
        - 📁 best_parameters -> dados dos modelos atuais
        - 📁 reports -> relatórios do treinamento dos modelos
    - 📁 funções -> arquivos para operação dos modelos
        - 📄 model_predict.py -> funções para desenvolvimento do modelo
        - 📄 utility.py -> funções básicas para operação do serviço
    - 📁 img -> banco de imagens do serviço
    - 📁 pages -> informações das páginas desenvolvidas pelo serviço
        - 📁 skmodelos -> modelos treinados para o serviço
        - 📄 2_◾_LOJA.py -> tela de operação dos modelos preditivos para lojas
        - 📄 3_◾_CATEGORIA.py -> tela de operação dos modelos preditivos para  categorias de produtos
        - 📄 4_◾_PRODUTO.py -> tela de operação dos modelos preditivos para produtos
    - 📁 tabelas_casting -> base de dados do modelo
        - 📄 lojas.json -> lista de lojas do modelo
        - 📄 tablelist.py -> função para criar o arquivo lojas.json    
    - 📄 1_◻️_INICIO.py -> tela inicial
    - 📄 dockerfile -> Gerando o container do serviço
    - 📄 main_update.py -> Arquivo para o módulo de treinamento do modelo
    - 📄 README.md -> Documentação do arquivo
    - 📄 requirements.txt -> dependências do serviço

## Fluxograma
![all txt](img/image.png)
    

## License

Time 13
