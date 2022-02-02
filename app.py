#from subprocess import HIGH_PRIORITY_CLASS
from ctypes.wintypes import HINSTANCE
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_apscheduler import APScheduler
from matplotlib.axis import Ticker
from sqlalchemy import false, true
import numpy as np

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
    # {
    #     "id": "yfinace-job-9AM", 
    #     "func": scheduleDataImportCronJob, 
    #     "trigger": "cron", 
    #     "hour": "09",
    #     "minute": "00",
    #     "day": "*",
    #     "timezone": "EST"
    # },
    {
        "id": "yfinace-job-midnight", 
        "func": scheduleDataImportCronJob, 
        "trigger": "cron", 
        "hour": "21",
        "minute": "30",
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

@app.route('/', methods = ['GET'])
def HomePage():
    return 'Welcome to API Homepage.. '

@app.route('/api/get-all-data', methods = ['GET'])
def GetListResource():
    from database import get_all_records
    return get_all_records().to_json()

@app.route('/api/data', methods = ['POST'])
def PostTickerResource():
    if request.method == 'POST':
        content = request.get_json('content')
        tick = content["ticker"]
        start_date = content['start']
        end_date = content['end']
        #print(str(ticker + " " + start_date + " " + end_date))
        from database import get_records
        data = get_records(ticker=tick, start=start_date, end=end_date).to_json(orient='records')
        return jsonify(data)

@app.route('/admin/load-data', methods = ['GET'])
def RunLoadJob():
    tick = request.args.get('ticker')
    from data_load_jobs import load_data_nightly
    return jsonify(load_data_nightly(tick))

if __name__ == '__main__' :
    scheduler.init_app(app)
    scheduler.start()
    dislpay_job_info()
    app.run(debug=True)
