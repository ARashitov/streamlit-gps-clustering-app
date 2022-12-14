
FROM --platform=linux/amd64 python:3.10.5

LABEL \
  maintainer="Adil Rashitov <adil.rashitov.98@gmail.com>" \
  title="streamlit-gps-clustering-app" \
  description="Dockerfile of streamlit app" \
  authors="Adil Rashitov <adil.rashitov.98@gmail.com>" \
  url="https://github.com/WasteLabs/dev_veolia_uk_lambda"

WORKDIR /app


ENV POETRY_VIRTUALENVS_CREATE=false

COPY ./ ./

RUN pip3 install --upgrade pip && pip3 install wheel poetry==1.2.2 && poetry install --only main

EXPOSE 8080

# ENTRYPOINT "python3 -m streamlit run --server.address 0.0.0.0 src/main.py"
