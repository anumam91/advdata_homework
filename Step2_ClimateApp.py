import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the 'Surf's Up' Climate App! <br/>"
        f"Available Routes:<br/>"
        f"For Precipiations Data from the Last 12 Months: /api/v1.0/precipitation <br/>"
        f"For A Complete List of Stations: /api/v1.0/stations <br/>"
        f"For Temperature Observations from the Busiest Station* from the Last 12 Months: /api/v1.0/tobs <br/>"
        f"*The Busiest Station (the one with the most activity/recorded observations) was USC00519281"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Returns dates and precipitation data from the past year"""
    # Query all dates and precipitation levels from the last year 
    precip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").order_by(Measurement.date).all()
    # Convert list of tuples into normal list
    all_precip = list(np.ravel(precip_data))

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    """Returns a list of stations from the dataset"""
    # Query all station names from dataset
    station_list = session.query(Measurement.station).distinct().all()
    all_stations = list(np.ravel(station_list))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    """Returns a list of temperature observations from the last year"""
    # Query all all dates and temperature observations from the last year
    tobs_list = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").filter(Measurement.station == 'USC00519281').order_by(Measurement.date).all()
    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(tobs_list))

    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug=True)
