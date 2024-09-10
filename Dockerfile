FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python3 -m pip install -r requirements.txt

USER appuser

COPY . .

ENV PORT=8000
ARG DISCORD_TOKEN

ENV DISCORD_TOKEN=${DISCORD_TOKEN}

EXPOSE ${PORT} 

CMD python3 app.py