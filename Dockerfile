FROM python:3.10

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY api_calls.py /app
COPY app.py /app
COPY index.py /app
COPY similarity.py /app
COPY generate_tensors.py /app
COPY secret.py /app
COPY tfidf_allcards /app
COPY .dockerignore /app

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "2", "app:app"]