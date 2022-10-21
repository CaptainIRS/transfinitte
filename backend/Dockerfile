FROM python:3.10-slim

ENV PYHTONUNBUFFERED=1
RUN apt-get update \
    && apt-get -y install gcc tesseract-ocr tesseract-ocr-eng tesseract-ocr-tam tesseract-ocr-hin tesseract-ocr-pan tesseract-ocr-ori \ 
    && apt-get -y install ffmpeg libsm6 libxext6

# tesseract-ocr required for pytesseract
# ffmpeg libsm6 libxext6 required for opencv

WORKDIR /app

COPY requirements.txt ./
COPY indic-trans/requirements.txt ./indic-trans/

RUN pip install -r requirements.txt -r indic-trans/requirements.txt
COPY indic-trans indic-trans
RUN cd indic-trans && pip install dist/indictrans*.tar.gz && cd ..

COPY . .

RUN apt-get install -y poppler-utils

CMD uvicorn app:app --host 0.0.0.0 --workers 2 --port 8000
