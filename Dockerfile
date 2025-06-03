FROM python:3.11-slim-bullseye as base

COPY requirements/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM base as app
COPY . /src/

ENV PYTHONPATH="/src/:/src/conversational_evaluation"
EXPOSE 8000

CMD ["uvicorn", "conversational_evaluation.main:app", "--host", "0.0.0.0", "--port", "8000"]