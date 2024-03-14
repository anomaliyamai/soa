FROM python:3.10
LABEL authors="olegafanasev"
WORKDIR /restapiservice/
COPY . .
RUN pip install sqlalchemy
RUN pip install "fastapi[all]"
RUN pip install psycopg2
CMD ["python", "app.py"]