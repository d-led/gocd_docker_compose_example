## up and running

```
docker-compose start
```

## access the instance

http://localhost:8153

- might take some time for the webserver to start

## shutdown

```
docker-compose stop
```

## todo

- [ ] build a customized server image with the [yaml config plugin](https://github.com/tomzo/gocd-yaml-config-plugin)
- [ ] bootstrap the pipeline either with  [gocdapi](https://github.com/joaogbcravo/gocdapi) or  [gomatic](https://github.com/SpringerSBM/gomatic) (drop the pipeline repo config XML blob or create the pipeline using any of the APIs)
- [ ] create a couple of custom agents
