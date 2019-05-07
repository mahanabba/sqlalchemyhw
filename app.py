import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route('/')
def available():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route('/api/v1.0/precipitation')
def precipitation():
    results = session.query(Measurement.prcp,Measurement.date).all()
    
    prcp_bydate = []
    for date in results:
        prcp_dict = {}
        prcp_dict['Date'] = Measurement.date
        prcp_dict['Prcp'] = Measurement.prcp
        prcp_bydate.append(prcp_dict)

    return jsonify(prcp_bydate)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.name).all()
    
    stationlist = list(np.ravel(results))

    return jsonify(stationlist)

@app.route('/api/v1.0/tobs')
def tobs():
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-03-05').all()
    
    temp_data = list(np.ravel(results))

    return jsonify(temp_data)

@app.route('/api/v1.0/<start>')
def start(start):
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    start_data = list(np.ravel(results))
    
    return jsonify(start_data)

@app.route('/api/v1.0/<start>/<end>')
def startend(start, end):
     results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    startend_data = list(np.ravel(results))

    return jsonift(startend_data)


if __name__ == '__main__':
    app.run(debug=True)
