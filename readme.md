# Project

This is a project for the module **ECM1400 Programming**.

# Plan

## Format of read data

{
"station" : [
(date_and_time, {
"no" : no_value,
"pm10" : pm10_value,
"pm25" : pm25_value
})
]
}

## Reporting Module

### daily_average(data, monitoring_station : str, pollutant : str) -> list (365 values)

Pseudocode:
Iterate over the list associated with the station.
Mean_daily_values = []
for i in 365:
normal_values = []
for j in 24:
Add values to a list.
Call meanvalue(list)
Add the return value to a list of mean_daily_values

### daily_median(data, monitoring_station : str, pollutant : str) -> list

### hourly_average(data, monitoring_station : str, pollutant : str) -> list

### monthly_average(data, monitoring_station : str, pollutant : str) -> list

### peak_hour_date(data, monitoring_station : str, pollutant : str) -> string (hour date)

### count_missing_data(data, monitoring_station : str, pollutant : str) -> int

### fill_missing_data(data, monitoring_station : str, pollutant : str) -> copy of data
