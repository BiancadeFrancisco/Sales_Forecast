FROM python:3.12.0

WORKDIR /forecasting

COPY . /forecasting

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit run", "1_◻️_INICIO.py"]


# Comando para buildar a imagem do serviço: docker build -t casting_forcasting .

# Comando para rodar o serviço: docker run casting_forcasting