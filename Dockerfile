FROM python:3.9

ENV PYTHONPATH=.
WORKDIR /app
RUN python3 -m pip install poetry && poetry config virtualenvs.create false


COPY pyproject.* /app/
RUN poetry install --no-dev

COPY . /app/


CMD ["python3", "-u", "-OO", "/app/run.py"]
