FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV TZ="America/Manaus"
RUN apt update && apt -y install libaio1

COPY . /var/www/

WORKDIR /var/www/

RUN apt-get update && apt-get install -y \
    software-properties-common \
    unzip \
    curl \
    xvfb

RUN curl https://dl-ssl.google.com/linux/linux_signing_key.pub -o /tmp/google.pub \
    && cat /tmp/google.pub | apt-key add -; rm /tmp/google.pub \
    && echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list \
    && mkdir -p /usr/share/desktop-directories \
    && apt-get -y update && apt-get install -y google-chrome-stable

RUN dpkg-divert --add --rename --divert /opt/google/chrome/google-chrome.real /opt/google/chrome/google-chrome \
    && echo "#!/bin/bash\nexec /opt/google/chrome/google-chrome.real --no-sandbox --disable-setuid-sandbox \"\$@\"" > /opt/google/chrome/google-chrome \
    && chmod 755 /opt/google/chrome/google-chrome

ENV DISPLAY=:99

RUN pip install -r requirements.txt

ADD main.py /

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "5", "--log-level", "debug"]