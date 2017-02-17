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

- [x] build a customized server image with the [yaml config plugin](https://github.com/tomzo/gocd-yaml-config-plugin)
- [x] bootstrap the pipeline with the [REST API](https://api.gocd.io/current)
- [x] create a couple of custom agents
