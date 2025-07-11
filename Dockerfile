  
FROM python:3.11 AS requirements-stage
 
WORKDIR /tmp
 
RUN pip install poetry

# Instala o plugin necessário para exportação
RUN poetry self add poetry-plugin-export
 
COPY ./pyproject.toml ./poetry.lock* /tmp/
 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
 
FROM python:3.11
 
WORKDIR /code
 
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
COPY ./app /code/app
 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
