from typing import Tuple
from os import listdir
from pandas import DataFrame, read_csv, read_excel, Index

def read_files() -> Tuple[DataFrame, DataFrame]:
    '''
    Dataframe structure:

    Meteo:
    STATION_NAME, YEAR, MONTH, DAY, PRECIPITATION

    Hydro:
    STATION_NAME, YEAR, MONTH, DAY, WATER_LEVEL
    '''

    files = listdir('data')

    if len(files) != 4:
        raise Exception('There should be 4 files in the data folder')

    meteo_file = files[next(i for i, v in enumerate(files) if v.startswith('meteo'))]
    hydro_file = files[next(i for i, v in enumerate(files) if v.startswith('hydro'))]
    meteo_stations_file = files[next(i for i, v in enumerate(files) if v == 'stations_meteo.txt')]
    hydro_stations_file = files[next(i for i, v in enumerate(files) if v == 'stations_hydro.txt')]

    meteo_stations = []
    hydro_stations = []
    meteo_data = []
    hydro_data = []
    filtered_meteo = DataFrame()
    filtered_hydro = DataFrame()

    with open('data/' + meteo_stations_file, 'r', encoding='utf-8') as f:
        meteo_stations = [line.rstrip('\n') for line in f.readlines()]

    with open('data/' + hydro_stations_file, 'r', encoding='utf-8') as f:
        hydro_stations = [line.rstrip('\n') for line in f.readlines()]

    if meteo_file.endswith('.csv'):
        meteo_data = read_csv('data/' + meteo_file, header = None, names = [
            'STATION_CODE',
            'STATION_NAME',
            'YEAR',
            'MONTH',
            'DAY',
            'PRECIPITATION',
            'SMDB',
            'PRECIPITATION_TYPE',
            'SNOW_DEPTH',
            'PKSN',
            'FRESH_SNOW_DEPTH',
            'HSS',
            'SNOW_CODE',
            'GATS',
            'SNOW_COVER_CODE',
            'RPSN'
        ])

        filtered_meteo = meteo_data[meteo_data['STATION_NAME'].isin(meteo_stations)][['STATION_NAME', 'YEAR', 'MONTH', 'DAY', 'PRECIPITATION']]
    elif meteo_file.endswith('.xlsx'):
        meteo_data = read_excel('data/' + meteo_file, sheet_name = 'dane', header = None)

        stations = [x[:x.index('(') - 1] for x in filter(lambda y: isinstance(y, str), meteo_data.values[0])]

        meteo_data.drop(index = [0, 1], inplace = True)
        meteo_data.reset_index(drop = True, inplace = True)

        dates = meteo_data[0].values
        years, months, days = [], [], []
        index = Index(range(1, len(meteo_data.columns), 2))
        values = meteo_data[index].values

        for date in dates:
            date = date.split('-')
            years.append(date[2])
            months.append(date[1])
            days.append(date[0])

        data = []

        for i in range(len(stations)):
            for ii in range(len(values)):
                data.append([stations[i], years[ii], months[ii], days[ii], values[ii][i]])

        filtered_meteo = DataFrame(data, columns = ['STATION_NAME', 'YEAR', 'MONTH', 'DAY', 'PRECIPITATION'])

    if hydro_file.endswith('.csv'):
        hydro_data = read_csv('data/' + hydro_file, header = None, names = [
            'STATION_CODE',
            'STATION_NAME',
            'STATION_RIVER',
            'YEAR',
            'MONTH',
            'DAY',
            'WATER_LEVEL',
            'WATER_FLOW',
            'WATER_TEMPERATURE',
            'CALENDAR_MONTH'
        ])

        filtered_hydro = hydro_data[hydro_data['STATION_NAME'].isin(hydro_stations)][['STATION_NAME', 'YEAR', 'MONTH', 'DAY', 'WATER_LEVEL']]
    elif hydro_file.endswith('.xlsx'):
        hydro_data = read_excel(
            'data/' + hydro_file,
            skiprows = 3,
            sheet_name = 'dane',
            header = None,
            names = [
                'DATE',
                'WATER_LEVEL_END',
                'WATER_LEVEL_START'
            ])

        dates = hydro_data['DATE'].values
        years, months, days = [], [], []

        for date in dates:
            date = date.split('-')
            years.append(date[0])
            months.append(date[1])
            days.append(date[2])

        water_levels_start = hydro_data['WATER_LEVEL_START'].values
        water_levels_end = hydro_data['WATER_LEVEL_END'].values

        data = []

        for i in range(len(water_levels_start)):
            data.append([hydro_stations[0], years[i], months[i], days[i], water_levels_start[i]])
        
        for i in range(len(water_levels_end)):
            data.append([hydro_stations[1], years[i], months[i], days[i], water_levels_end[i]])

        filtered_hydro = DataFrame(data, columns = ['STATION_NAME', 'YEAR', 'MONTH', 'DAY', 'WATER_LEVEL'])

    filtered_meteo = filtered_meteo.fillna(0)
    filtered_hydro = filtered_hydro.fillna(0)

    return filtered_meteo, filtered_hydro

