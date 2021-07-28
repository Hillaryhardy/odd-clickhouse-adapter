## ODD ClickHouse adapter

ODD ClickHouse adapter is used for extracting datasets and and data transformers info and metadata from Yandex ClickHouse. This adapter is implemetation of pull model (see more https://github.com/opendatadiscovery/opendatadiscovery-specification/blob/main/specification/specification.md#discovery-models). By default application gather data from ClickHouse every minute, put it inside local cache and then ready to give it away by /entities API.

This service based on Python Flask and Connexion frameworks with APScheduler.

#### Data entities:
| Entity type | Entity source |
|:----------------:|:---------:|
|Dataset|Tables, Columns|
|Data Transformer|Views|

For more information about data entities see https://github.com/opendatadiscovery/opendatadiscovery-specification/blob/main/specification/specification.md#data-model-specification

## Quickstart
Application is ready to run out of the box by the docker-compose (see more https://docs.docker.com/compose/).
Strongly recommended to override next variables in docker-compose .env file:

CLICKHOUSE_DATABASE = oddadapter #name of your ClickHouse database.
CLICKHOUSE_USER = oddadapter #username of your ClickHouse database.
CLICKHOUSE_PASSWORD = odd-adapter-password #password of your ClickHouse database.

CLOUD_TYPE = aws #Name of your cloud service. Used to form ODDRN.
CLOUD_REGION = region_1 #Region of your cloud service. Used to form ODDRN.
CLOUD_ACCOUNT =account_1 #Account of your cloud service. Used to form ODDRN.

After docker-compose run successful, application is ready to accept connection on port :8080.

## Environment
Adapter is ready to work out of box, but you probably will need to redefine some variables in compose .env file:

```Python
FLASK_ENVIRONMENT = development # For production case change this to "production"

CLICKHOUSE_HOST = db #host of your ClickHouse database.
CLICKHOUSE_PORT = 9000 #port of your ClickHouse database.
CLICKHOUSE_DATABASE = oddadapter #name of your ClickHouse database.
CLICKHOUSE_USER = oddadapter #username of your ClickHouse database.
CLICKHOUSE_PASSWORD = odd-adapter-password #password of your ClickHouse database.

CLOUD_TYPE = aws //Name of your cloud service. Used to form ODDRN.
CLOUD_REGION = region_1 //Region of your cloud service. Used to form ODDRN.
CLOUD_ACCOUNT = account_1 //Account of your cloud service. Used to form ODDRN.
```

## Helm chart
Link to Helm config https://github.com/opendatadiscovery/charts

## Requirements
- Python 3.8
- ClickHouse 21.6