# Как запустить

Из папки сервиса:

`docker-compose up -d`

Можно смотреть что происходить в БД при помощи команды:

`docker-compose exec db psql --username=postgres --dbname=postgres`

А дальше уже обращаться по сырым запросам SQL.