FROM python:3.11.9-alpine3.19

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

COPY twitter /twitter
COPY scripts /scripts

WORKDIR /twitter

EXPOSE 8000

RUN python -m venv /venv && \
  /venv/bin/pip install --upgrade pip && \
  /venv/bin/pip install -r /twitter/requirements.txt && \
  adduser --disabled-password --no-create-home duser && \
  mkdir -p /staticfiles && \
  mkdir -p /data/media && \
  chown -R duser:duser /venv && \
  chown -R duser:duser /staticfiles && \
  chown -R duser:duser /data/media && \
  chmod -R 755 /staticfiles && \
  chmod -R 755 /data/media && \
  chmod -R +x /scripts

ENV PATH="/scripts:/venv/bin:$PATH"

USER duser

CMD ["commands.sh"]