# FastAPI App

## Запуск

В проект добавлен файл `config.yaml` для настройки приложения

````yaml

```bash
cp .env.example .env
````

```bash
docker-compose up --build
```

## Тесты

```bash
docker-compose -f "docker-compose.tests.yml" up --build
```
