## Подписка из браузера на pub/sub valkey

пример сервиса - **main.py**

пример клиента - **redis_demo.html**

compose - файл для запуска valkey в каталоге **valkey**

публиковать в redis/vallkey можно любым подходящим для этого средством, например [Redis Insight](https://github.com/redis/RedisInsight). 

```mermaid
architecture-beta
    service valkey(database)[Valkey]
    service server(server)[PubService]
    service browser(internet)[Browser]
    service events1(server)[Event source]
    service events2(server)[Event source 2]

    events1:L --> R:valkey
    valkey:L <-- R:events2
    valkey:B --> T:server
    server:B --> T:browser   
```