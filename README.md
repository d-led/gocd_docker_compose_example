## up and running

```
docker-compose up -d
```

## access the instance

- [http://localhost:8153](http://localhost:8153)
- the webserver might take some time to start

## shutdown

```
docker-compose stop
```

or destroy via:

```
docker-compose down --remove-orphans
```

## todo

- [ ] build a customized server image with the [yaml config plugin](https://github.com/tomzo/gocd-yaml-config-plugin)
- [ ] bootstrap the pipeline either with  [gocdapi](https://github.com/joaogbcravo/gocdapi) or  [gomatic](https://github.com/SpringerSBM/gomatic) (drop the pipeline repo config XML blob or create the pipeline using any of the APIs)
- [ ] create a couple of custom agents
