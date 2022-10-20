FROM python:3.10-slim

ENV PYHTONUNBUFFERED=1
RUN apt-get update \
    && apt-get -y install tesseract-ocr  \ 
    && apt-get -y install ffmpeg libsm6 libxext6

# tesseract-ocr required for pytesseract
# ffmpeg libsm6 libxext6 required for opencv

WORKDIR /app

COPY requirements.txt indic-trans/requirements.txt ./

RUN pip install -r requirements.txt -r indic-trans/requirements.txt
RUN cd indic-trans && python setup.py install && cd ..

COPY . .

RUN uvicorn app:app --host 0.0.0.0 --workers 2 --port 8000cdc
