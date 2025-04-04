FROM python:alpine
RUN apk --no-cache add chromium chromium-chromedriver tini build-base libffi-dev
RUN pip install flask && pip install selenium==4.10.0

WORKDIR /usr/src/app
COPY ./src .

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python","main.py"]