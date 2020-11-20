#put flask app here (all of Step 2 - Climate app)
from flask import Flask, render_template, jsonify
import sqlalchemy
from sqlalchemy import create_engine, func, inspect, distinct, Table, MetaData, Column, Integer
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt
import pandas as pd

app = Flask(__name__)

@app.route('/')
def root():
    return '''
        <!DOCTYPE html>
        <html class lang="en-us">
        <head>
            <title>Home</title>
        </head>
        <div>
            <h3>Pages</h3>
            <ul>
                <li>Precipitation Data</li>
                <ul><li>/api/v1.0/precipitation</li></ul>
                <li>Weather Stations</li>
                <ul><li>/api/v1.0/stations</li></ul>
                <li>Temperature Data for Most Active Weather Station</li>
                <ul><li>/api/v1.0/tobs</li></ul>
                <li>Temperature Data After Specified Date</li>
                <ul><li>/api/v1.0/&ltstart&gt</li></ul>
                <li>Temparature Data in Date Range</li>
                <ul><li>/api/v1.0/&ltstart&gt/&ltend&gt</li></ul>
            </ul>
        </div>
    '''

@app.route('/api/v1.0/precipitation')
def apiv10precipitation():
    #connect to sqlite, reflect existing DB and tables
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect = True)
    measurement = Base.classes['measurement']
    session = Session(bind = engine)

    #calculate the date 1 year ago from the last data point in the database
    lastDateText = session.query(func.max(measurement.date)).all()[0][0]
    lastDateDT = dt.datetime.fromisoformat(lastDateText)
    firstDateDT = dt.datetime(lastDateDT.year - 1, lastDateDT.month, lastDateDT.day)
    firstDateText = firstDateDT.isoformat()[0:10]

    #find all station names
    stationCodes = session.query(measurement.station).group_by(measurement.station).all()

    #create dataframe with first city, merge dataframes for next cities with the original dataframe
    firstStation = True
    for stationCode in stationCodes:
        # Perform a query to retrieve the data and precipitation scores for city
        prcpQuery = session.query(measurement.date, measurement.prcp).\
                        filter(measurement.date > firstDateText, measurement.station == stationCode[0])

        if firstStation:
            # Save the query results as a Pandas DataFrame for first city precipitation data 
            oneYearPrcpData = pd.read_sql(prcpQuery.statement, prcpQuery.session.bind)
            oneYearPrcpData.rename(columns = {'prcp': stationCode[0]}, inplace = True)
            firstStation = False
            
        else:
            # Save the query results as a Pandas DataFrame and merge with dataframe of previous city columns
            tempOneYearPrcpData = pd.read_sql(prcpQuery.statement, prcpQuery.session.bind)
            oneYearPrcpData = pd.merge(oneYearPrcpData, tempOneYearPrcpData, on = 'date', how = 'outer')
            #rename precipitation column to city code
            oneYearPrcpData.rename(columns = {'prcp': stationCode[0]}, inplace = True)
        #set date as dataframe index, sort the dataframe by date
        oneYearPrcpData.set_index('date', inplace = True)
        oneYearPrcpData.sort_index()
        #convert to dict then json
        oneYearPrcpDataDict = oneYearPrcpData.T.to_dict('index')
        oneYearPrcpDataJson = jsonify(oneYearPrcpDataDict)
    return oneYearPrcpDataJson

@app.route('/api/v1.0/stations')
def apiv10stations():
    #connect to sqlite, reflect existing DB and tables
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect = True)
    station = Base.classes['station']
    session = Session(bind = engine)

    #find all stations and convert to Json
    stationsDict = dict(session.query(station.station, station.name).all())
    stationJson = jsonify(stationsDict)

    return stationJson

@app.route('/api/v1.0/tobs')
def apiv10tobs():
    #connect to sqlite, reflct existing DB and tables
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect = True)
    measurement = Base.classes['measurement']
    session = Session(bind = engine)

    #find station with most observations
    stationRowCount = session.query(measurement.station, func.count(measurement.station)).\
                        group_by(measurement.station).\
                        order_by(func.count(measurement.station).desc())
    topStation = stationRowCount.first()[0]

    #calculate the date 1 year ago from the last data point in the database
    lastDateText = session.query(func.max(measurement.date)).all()[0][0]
    lastDateDT = dt.datetime.fromisoformat(lastDateText)
    firstDateDT = dt.datetime(lastDateDT.year - 1, lastDateDT.month, lastDateDT.day)
    firstDateText = firstDateDT.isoformat()[0:10]

    #find temps of station in the last year
    topStationTemps = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date > firstDateText, measurement.tobs != sqlalchemy.sql.null(), measurement.station == topStation)
    #display query as Json
    topStationTempsJson = jsonify(dict(topStationTemps.all()))
    return topStationTempsJson

@app.route('/api/v1.0/<start>')
def apiv10start(start):
    #connect to sqlite, reflct existing DB and tables
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect = True)
    measurement = Base.classes['measurement']
    session = Session(bind = engine)

    #find temperature summary statistics of dates after start date
    tempStatsAfterDate = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start)
    tmin, tavg, tmax = tempStatsAfterDate.all()[0]

    #construct summary statistics Json
    tempStatsAfterDateJson = jsonify({'tmin': tmin, 'tavg': tavg, 'tmax': tmax})

    return tempStatsAfterDateJson

@app.route('/api/v1.0/<start>/<end>')
def apiv10startend(start, end):
    #connect to sqlite, reflct existing DB and tables
    engine = create_engine("sqlite:///Resources/hawaii.sqlite")
    Base = automap_base()
    Base.prepare(engine, reflect = True)
    measurement = Base.classes['measurement']
    session = Session(bind = engine)

    #find temperature summary statistics of dates in date range
    tempStatsAfterDate = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end)
    tmin, tavg, tmax = tempStatsAfterDate.all()[0]

    #construct summary statistics Json
    tempStatsRangeDateJson = jsonify({'tmin': tmin, 'tavg': tavg, 'tmax': tmax})

    return tempStatsRangeDateJson

app.run(debug = True)