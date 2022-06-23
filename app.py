
import datetime as dt
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session

from flask import Flask, jsonify
engine = create_engine("sqlite:///../Instructions/Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurements = Base.classes.measurement
Stations = Base.classes.station

session = Session(engine)

app = Flask(__name__)
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for last year"""
    latest_12months = dt.date(2017,8,23) - dt.timedelta(days = 365)

    latest_data = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date > latest_12months).all()

    session.close()

    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    """Return list of stations."""
    stations_list = session.query(Stations.station).all()

    session.close()

    stations = list(np.ravel(stations_list))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return temperature observations (tobs) for last 12 months."""
    latest_12months = dt.date(2017,8,23) - dt.timedelta(days = 365)

    USC00519281_12months = session.query(Measurements.tobs).\
    filter((Measurements.date > latest_12months) & (Measurements.station == "USC00519281")).all()

    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    stats = [func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)]

    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = session.query(*stats).\
            filter(Measurements.date >= start).all()

        session.close()

        temps = list(np.ravel(results))
        return jsonify(temps)

    start = dt.datetime.strptime(start, "%m%d%Y")
    end = dt.datetime.strptime(end, "%m%d%Y")

    results = session.query(*stats).\
        filter(Measurements.date >= start).\
        filter(Measurements.date <= end).all()

    session.close()

    temps = list(np.ravel(results))
    return jsonify(temps=temps)
    
if __name__ == '__main__':
    app.run()
 