FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY . /app

EXPOSE 3000
CMD ["bentoml", "serve", "seattle_energy.service:EnergyService", "--port", "3000", "--production"]