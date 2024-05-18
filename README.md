## Create virtualenv:
```shell
python3 -m venv .venv
```

## Activate virtual env:
```shell
source .venv/bin/activate
```
## Install dependencies:
```shell
pip install -r requirements.txt
```

## Copy .env.example as .env
> copy `.env_example` as `.env`


## Migrate db

```shell
alembic upgrade head 
```

## Run

```shell
python main.py
```

## Docs location:
> http://localhost:8000/docs

> http://localhost:8000/redoc
