# Geneology Tree
Простое приложение на FastAPI с PostgreSQL для реализации генеологического дерева.
Также содержит простого бота для Telegram, который выводит родословную по имени человека.

1. Создайте ТГ бота через @BotFather и внесите токен в `docker-compose.yml`:
```compose
bot:
    build: .
    environment:
      - BOT_TOKEN=*сюда токен*
```

2. Запустите всё приложение:
```bash
docker-compose up --build
```

3. Для тестового заполнения БД можно использовать скрипт:
```bash
source api_fill.sh
```
