# FastAPI manual

## command
- run the server
```
uvicorn main:app --reload
```
- run server with options
```
uvicorn main:app --reload --host=0.0.0.0 --port=8080
```
- run prod server
```
gunicorn -k uvicorn.workers.UvicornWorker --access-logfile ./gunicorn-access.log main:app --bind 0.0.0.0:8080 --workers 2 --daemon
```

## API Documentation
> use Swagger UI

- url
[http://127.0.0.1:8000/docs]

## migration
[ref](https://blog.neonkid.xyz/257?utm_source=pocket_mylist)
> use alembic
- generate script
```
alembic revision --autogenerate -m "initialize entity"
```
- upgrade
```alembic upgrade head```
- downgrade
```alembic downgrade [revision_hash or current_revision +- 1]```

## 작업 현황
[click here](doc/work.md)

## 우분투 mysqlclient에러 관련 추가 설치 사항
https://www.sysnet.pe.kr/Default.aspx?mode=2&sub=0&pageno=0&detail=1&wid=12850

## docker 배포
https://linuxtut.com/en/02ed76b94c60deba8282/

### RUN
```
# `app`Build image of
docker-compose build

#Starting the entire service
docker-compose up -d

#When finished
docker-compose down

#Check console output
docker-compose logs
docker-compose logs app #Check only app service log

#Go inside the app container
docker-compose run app bash
```
