## Подписка из браузера на pub/sub vallkey

пример сервиса - **main.py**

пример клиента - **redis_demo.html**

публиковать в redis/vallkey можно любым подходящим для этого средством, например _Redis Insight_. 

```mermaid
architecture-beta
    service valkey(database)[Valkey]
    service server(server)[PubService]
    service browser(internet)[Browser]
    service events(server)[Event source]

    events:L --> R:valkey
    valkey:L --> R:server
    server:B --> T:browser
```