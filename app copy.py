#from subprocess import HIGH_PRIORITY_CLASS
from ctypes.wintypes import HINSTANCE
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_apscheduler import APScheduler
from matplotlib.axis import Ticker
from sqlalchemy import false, true

app = Flask(__name__)
scheduler = APScheduler()

def dislpay_job_info():
   print('interval job')

   for job in scheduler.get_jobs():
        print("name: %s, trigger: %s, next run: %s, handler: %s" % (
          job.name, job.trigger, job.next_run_time, job.func))

def scheduleDataImportCronJob():
    from data_load_jobs import load_data_nightly
    load_data_nightly()
    
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datastore/ov_daily_data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5432/rajandevkota'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JOBS'] = [
    # {
    #     "id": "yfinace-job-test", 
    #     "func": scheduleDataImportCronJob, 
    #     "trigger": "cron", 
    #     "hour": "23",
    #     "minute": "40",
    #     "day": "*",
    #     "timezone": "EST"
    # },
    {
        "id": "yfinace-job-9AM", 
        "func": scheduleDataImportCronJob, 
        "trigger": "cron", 
        "hour": "09",
        "minute": "00",
        "day": "*",
        "timezone": "EST"
    },
    {
        "id": "yfinace-job-4PM", 
        "func": scheduleDataImportCronJob, 
        "trigger": "cron", 
        "hour": "16",
        "minute": "38",
        "day": "*",
        "timezone": "EST"
    }
]

app.config['SCHEDULER_API_ENABLED'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
from flask_migrate import Migrate
migrate = Migrate(app, db)

class DailyHistory(db.Model):
    Ticker = db.Column(db.String(100), primary_key=True)
    Date = db.Column(db.String(50), primary_key=True)
    Open = db.Column(db.String(100))
    High = db.Column(db.String(100))
    Low = db.Column(db.String(100))
    Close = db.Column(db.String(100))
    Adj_Close = db.Column(db.String(100))
    Volume = db.Column(db.String(100))

    def __repr__(self):
        return '<Post %s>' % self.ticker


class DailyHistorySchema(ma.Schema):
    class Meta:
        fields = ("Ticker", "Date","Open", "High", "Low", "Close", "Adj_Close", "Volume")


post_schema = DailyHistorySchema()
posts_schema = DailyHistorySchema(many=True)


class PostListResource(Resource):
    def get(self):
        posts = DailyHistory.query.all()
        return posts_schema.dump(posts)

    def post(self):
        new_post = DailyHistory(
            ticker=request.json['Ticker'],
            day=request.json['Date'],
            open=request.json['Open'],
            high=request.json['High'],
            low=request.json['Low'],
            close=request.json['Close'],
            adj_close=request.json['Adj_Close'],
            volume=request.json['Volume']          
        )
        db.session.add(new_post)
        db.session.commit()
        return post_schema.dump(new_post)

class PostResource(Resource):
    def get(self, post_id):
        hist = DailyHistory.query.get_or_404(post_id)
        return post_schema.dump(hist)

    def patch(self, post_id):
        hist = DailyHistory.query.get_or_404(post_id)

        if 'ticker' in request.json:
            hist.ticker = request.json['ticker']
        if 'date' in request.json:
            hist.day = request.json['date']
        if 'open' in request.json:
            hist.open = request.json['open']
        if 'high' in request.json:
            hist.high = request.json['high']
        if 'low' in request.json:
            hist.low = request.json['low']
        if 'adj_close' in request.json:
            hist.adj_close = request.json['adj_close']
        if 'volume' in request.json:
            hist.volume = request.json['volume']

        db.session.commit()
        return post_schema.dump(hist)

    def delete(self, post_id):
        hist = DailyHistory.query.get_or_404(post_id)
        db.session.delete(hist)
        db.session.commit()
        return '', 204

api.add_resource(PostListResource, '/history')
api.add_resource(PostResource, '/history/<int:post_id>')
# api.add_resource(PostListResource, '/get-daily-data/<str:ticker>/<str:start-date>/<str:end-date>')



if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    dislpay_job_info()
    app.run(debug=True)
