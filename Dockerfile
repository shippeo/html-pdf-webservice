FROM ubuntu:14.04
MAINTAINER Nathan Jones <nathan@ncjones.com>

# Install wkhtmltox + additional fonts + wkhtmltox + python-pip
RUN \
    apt-get update && \ 
    apt-get install -y wget && \
    wget -O wkhtmltox.deb https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.2.1/wkhtmltox-0.12.2.1_linux-trusty-amd64.deb && \
    apt-get install -y fontconfig libfontconfig1 libfreetype6 libjpeg-turbo8 libx11-6 libxext6 libxrender1 xfonts-base xfonts-75dpi fonts-wqy-zenhei fonts-thai-tlwg && \
    dpkg -i wkhtmltox.deb && \ 
    apt-get install -y python-pip && \ 
    echo "===> clean up..."  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install werkzeug gunicorn
RUN useradd gunicorn

ADD app.py /app.py
ADD config.py /config.py

EXPOSE 8080
USER gunicorn
ENTRYPOINT ["gunicorn"]
CMD ["-c", "/config.py", "app:application"]
