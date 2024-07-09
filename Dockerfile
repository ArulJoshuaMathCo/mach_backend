FROM python:3.10.12-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

# Run uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]