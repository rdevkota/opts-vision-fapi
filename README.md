# Blog REST API

Fully functional CRUD RESTful API with Flask and SQLAlchemy.

Wonder how I built this? checkout this [blog post](https://rahmanfadhil.com/flask-rest-api/)



 python -m venv env

 source env/bin/activate

$ python
>>> from app import db
>>> db.create_all()
>>> exit()

curl https://opts-vision-fapi.herokuapp.com/history
curl http://localhost:5000/history

curl http://localhost:5000/get-data/AMD

curl POST http://localhost:5000/get-data -d {"ticker": "AMD", "start": "12/01/02", "end": "2022/01/31"}

curl http://localhost:5000/get-data -X POST --data '{"ticker": "AMD", "start": "12/01/02", "end": "2022/01/31"}'

####
curl http://localhost:5000/api/get-all-data
curl http://localhost:5000/get-data/AMD
curl http://localhost:5000/api/data -X POST --data '{"ticker": "AMD", "start": "12/01/02", "end": "2022/01/31"}'

curl -d '{"ticker": "AMD"}' -H "Content-Type: application/json" -X POST http://localhost:5000/data

curl http://localhost:5000/api/data -X POST  -H "Content-Type: application/json" --data '{"ticker": "AMD", "start": "2022/01/25", "end": "2022/01/31"}'

curl http://localhost:5000/admin/load-data?ticker=FB
drop table daily_history;

-- public.daily_history definition

-- Drop table

-- DROP TABLE public.daily_history;

CREATE TABLE public.daily_history (
	"Date" timestamp NOT NULL,
	"Open" float8 NULL,
	"High" float8 NULL,
	"Low" float8 NULL,
	"Close" float8 NULL,
	"Adj Close" float8 NULL,
	"Volume" int8 NULL,
	"Ticker" text NOT NULL,
	CONSTRAINT daily_history_un UNIQUE ("Date", "Ticker")
);
CREATE INDEX "ix_daily_history_Date" ON public.daily_history USING btree ("Date");

select * from daily_history;



flask db stamp head
$ flask db init
$ flask db migrate
$ flask db upgrade



#heroky postgres
export DATABASE_URL=postgres://postgres:postgres@localhost:5432/rajandevkota

heroku config | grep HEROKU_POSTGRESQL

heroku pg:credentials:url DATABASE --app opts-vision-fapi
   postgres://fuzjujlciewljd:c25a57adb7262edbda0b3b1e099b121e1aeb61dca383690d47fcb2d99e5b1657@ec2-50-19-171-158.compute-1.amazonaws.com:5432/d42qtgtj7u9mrh


curl https://opts-vision-fapi.herokuapp.com/api/data -X POST  -H "Content-Type: application/json" --data '{"ticker": "FB", "start": "2022/01/25", "end": "2022/01/31"}'

curl https://opts-vision-fapi.herokuapp.com/api/real-time-data -X POST  -H "Content-Type: application/json" --data '{"ticker": "FB", "start": "2022/01/25", "end": "2022/01/31"}'

curl http://localhost:5000/api/real-time-data -X POST  -H "Content-Type: application/json" --data '{"ticker": "FB", "start": "2022-01-25", "end": "2022-01-31"}'

curl https://opts-vision-fapi.herokuapp.com/admin/load-data?ticker=FB