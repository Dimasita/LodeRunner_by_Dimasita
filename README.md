# Бот для игры LodeRunner 

## Что это
Бот для хакатона от компании EPAM, который высчитывает наилучший путь для сбора монет в игре LodeRunner против таких же ботов.   

## Установка
### Python
Для запуска бота необходимо наличие пакета websocket.   
pip install websockets

### Node.js
Для удобства проверки работоспособности бота написал простой сервер на Node и js скрипт для работы с ним через браузер.    
Запустить сервер можно либо напрямую через Node, либо через Docker.   
Docker файл для создания контейнера лежит в папке server.   
Для запуска сервера через Docker необходимо выполнить селдующие команды:   
  docker build -t name path/to/dockerfile   
  docker run -dp 3000:3000 name   
   
      
Далее можно будет подключиться к нему через браузер по адресу:   
localhost:3000   
