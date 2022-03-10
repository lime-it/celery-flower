# Come provare Celery + Flower

Dopo aver clonato il progetto eseguire il comando:

```
docker-compose up -d
```

Partiranno 3 container: 
* 1 nodo redis (equivalente rabbitmq, ma meno pesante per provare in locale)
* 1 nodo celery che espone i task di esempio che trovate nella cartella src
* 1 nodo celery che espone flower interfaccia + api

Per provare la UI di Flower vi basta accedere a [http://localhost:5555](http://localhost:5555)

Per provare le api basta invocarle usando come base url **http://localhost:5555/api**

Vi consiglio di provare il task **tasks.sleep_wh**, con un esempio di webhook, che spero vi facciano usare.

Esempio d'uso con curl:
```
curl -X POST http://localhost:5555/api/task/async-apply/tasks.sleep_wh \
 -H 'Content-Type: application/json' \
 -d '{"args":[5,"http://host.docker.internal:9999/prova"]}'
```

Qui **host.docker.internal** è il dns interno al container per il localhost su cui gira docker (il vostro localhost insomma). Questo task, a fine operazioni (uno sleep di enne secondi dati dal primo parametro), fa una richiesta http post al secondo parametro, come notifica di fine operazioni che vi evita il polling.