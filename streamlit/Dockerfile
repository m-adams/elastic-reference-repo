# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*


COPY ./requirements.txt .
RUN pip3 install -r ./requirements.txt

EXPOSE 8501
COPY ./[[STREAMLIT_FILENAME_HERE]] .

# Don't forget to copy anything else the file need like models, etc.

ENTRYPOINT ["streamlit", "run", "elastic_gpt.py", "--server.port=8501", "--server.address=0.0.0.0"]
