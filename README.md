# SQLAlchemy Challenge

# Overview

This project focuses on using sqlalchemy ORM queries to obtain and visualize temperature and precipitation data from a SQLite database of multiple weather stations in Hawaii. There is a table for daily weather measurements and a table for weather station data.

## Set up SQLalchemy connection

* Automap existing SQLite tables into the SQLalchemy base

* Inspect tables to get familiar with tables, columns and data types.

* Name the measurement and station tables to be used in the analysis

* Start the SQLalchemy session

## Precipitation Analysis

* Design a query to retrieve the last 12 months of precipitation data.

* Load the query results into a Pandas DataFrame and set the index to the date column.

* Sort the DataFrame values by date.

* Plot the results to a line graph

* Use Pandas to print the summary statistics for the precipitation data.

## Station Analysis

* Design a query to calculate the total number of stations.

* Design a query to find the most active stations.

  * List the stations and observation counts in descending order.

  * Find the station with the highest number of observations

* Design a query to retrieve the last 12 months of temperature observation data (TOBS).

  * Filter by the station with the highest number of observations.

  * Plot the results as a histogram with 12 bins.

## Trip Analysis

* Choose a start date and end date for the trip

* Use a bar chart with an error range to visualize the average temperature and temperature error over the trip

* Find the total rainfall at each weather station over the trip

* Calculate daily normals for each day of the trip and plot to a stacked area plot

## Climate App

* Use Flask to create the following routes:

### Routes

* `/`

  * Home page

  * List all routes that are available

* `/api/v1.0/precipitation`

  * Display precipitation values for each day for each station in JSON format

* `/api/v1.0/stations`

  * Display a JSON list of all stations

* `/api/v1.0/tobs`

  * Display temperature values for each day of the last year for each station in JSON format

* `/api/v1.0/<start>`

  * Display temperature summary statistics(`TMIN`, `TAVG`, and `TMAX`) for all days following the start date injected to the URL, in JSON format

* `/api/v1.0/<start>/<end>`

  * Display temperature summary statistics(`TMIN`, `TAVG`, and `TMAX`) for all days in the date range injected to the URL, in JSON format
