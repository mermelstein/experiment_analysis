FROM python:3.7-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip==21.0

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app/src

ENV PATH /app:$PATH

USER root

EXPOSE 8000

RUN chmod -R 777 .

RUN TEMP_DEB="$(mktemp)"; \
  wget -O "$TEMP_DEB" 'https://github.com/quarto-dev/quarto-cli/releases/download/v0.9.165/quarto-0.9.165-linux-amd64.deb'; \
  dpkg -i "$TEMP_DEB"; \
  rm -f "$TEMP_DEB"

CMD python main.py