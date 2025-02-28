# Build Stage
FROM node:18-alpine AS build
WORKDIR /app
COPY . ./
RUN npm install
RUN npm run build

# Production Stage
FROM python:3.11.9-bullseye AS production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY=false-secret
WORKDIR /app
COPY . ./
COPY --from=build /app/build/ ./build/
RUN apt-get update && apt-get install -y weasyprint \
    && pip install -r requirements.txt \    
    && python manage.py collectstatic \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000
ENTRYPOINT ["sh", "./entrypoint.sh"]