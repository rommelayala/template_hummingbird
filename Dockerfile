FROM docker.registry.vptech.eu/python:3.11.3-slim-bullseye

RUN apt-get update -qq --fix-missing \
 && apt-get -qq -y install --no-install-recommends tzdata \
 && python3 -m pip install --upgrade pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY . /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt \
 && playwright install --with-deps chromium

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python3", "tests/test_campaings.py"]
