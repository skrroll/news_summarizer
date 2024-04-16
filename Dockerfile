FROM python:3.12
WORKDIR /app
EXPOSE 465
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]