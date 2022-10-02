FROM python:3.8-alpine
MAINTAINER Ivan Hahanov 'ivanhahanov13@gmail.com'
COPY app /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN echo "flag{L0c@l_F1l3_Inclu$10n}" >> /etc/passwd
CMD python3 server.py