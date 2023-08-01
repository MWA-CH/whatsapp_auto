FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY whatsapp_auto.py ./

CMD streamlit run whatsapp_auto.py