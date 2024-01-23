FROM python:3.7.6-slim
RUN mkdir /var/tmp/RSIAPP
RUN mkdir /app/
ADD main.py /app/
ADD getrsimod.py /app/
ADD config.py /app/
ADD launch.sh /app/
ADD templates /app/templates
ADD static /app/static
ADD requirements.txt /app/
WORKDIR /app
RUN chmod +x launch.sh
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN openssl req -x509 -nodes -days 365 -subj "/C=CA/ST=ON/O=CompanyName, Inc./CN=173.30.15.205" -addext "subjectAltName=DNS:172.30.15.205" -newkey rsa:2048 -keyout key.pem -out cert.pem -addext "extendedKeyUsage = serverAuth"

EXPOSE 5000
ENTRYPOINT [ "./launch.sh" ]
