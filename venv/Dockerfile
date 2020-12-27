FROM python:3.6-slim
WORKDIR /venv
COPY . /venv
RUN pip install --no-cache-dir flask flask_restful matplotlib pandas numpy scipy xgboost
EXPOSE 5000
CMD ["python3","run.py"]