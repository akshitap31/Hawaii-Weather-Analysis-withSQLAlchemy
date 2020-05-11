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
Station=Base.classes.station
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def date_perc():
    session=Session(engine)
    results=session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    percp_list=[]

    for date, per in results:
        prcp_dict = {}
        prcp_dict["date"]=date
        prcp_dict["prcp"]=per
        percp_list.append(results)
    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    session=Session(engine)
    stations=session.query(Station.station, Station.name).all()
    session.close()
    all_stations=list(np.ravel(stations))
    return jsonify(all_stations)
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # find which station is the most active/has the most TOBs
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()
    # find TOB per day for the past 12 months for the most active station
    tob_12month = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station==most_active_station[0]).\
        filter(Measurement.date > '2016-08-18').\
        order_by(Measurement.date.desc()).all()
    session.close()
    tobs_list = []
    for date, tobs in tob_12month:
        tob_12month = {}
        tob_12month["date"] = date
        tob_12month["TOB"] = tobs
        tobs_list.append(tob_12month)

    return jsonify(tobs_list)
@app.route("/api/v1.0/<start>")
def temps(start):
    session=Session(engine)
    t=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date == start )
    session.close()
    temp_list=[]
    for min, max, avg in t:
        tob={}
        tob["TMIN"]=min
        tob["TMAX"]=max
        tob["TAVG"]=avg
        temp_list.append(tob)
    return jsonify(temp_list)
@app.route("/api/v1.0/<start>/<end>")
def holiday(start, end):
    session=Session(engine)
    holiday_t=session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start ).filter(Measurement.date <= end )
    session.close()
    temp=[]
    for min, max, avg in holiday_t:
        temp_dict={}
        temp_dict["TMIN"]=min
        temp_dict["TMAX"] = max
        temp_dict["TAVG"] = avg
        temp.append(temp_dict)
    return jsonify(temp)