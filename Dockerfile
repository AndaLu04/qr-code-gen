FROM debian:stable-slim
ADD ./code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python3 main.py