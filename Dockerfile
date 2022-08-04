FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /katyabot
COPY requirements.txt /katyabot
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /katyabot
CMD ["python3","run.py"]