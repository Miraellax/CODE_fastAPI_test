# FROM python:3.10
#
# WORKDIR /src
#
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
#
# COPY ./requirements.txt ./requirements.txt
#
# RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
#
# COPY ./app /app
#
# CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
# # CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# CMD ["fastapi", "run", "app/main.py", "--port", "80"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
