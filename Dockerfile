FROM python:3.10-slim
LABEL authors="Theesh Thilakarathne"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VERSION=1.1.11

RUN pip install "poetry==$POETRY_VERSION"
RUN pip install --upgrade poetry
WORKDIR /app

COPY . /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev


#uvicorn main:app --host 0.0.0.0 --port 8000

#CMD ["uvicorn", "main:app", "--host 0.0.0.0", "--port 8000"]

#ENTRYPOINT ["tail", "-f", "/dev/null"]