from pandas import DataFrame, Series, read_csv, concat
from datetime import datetime

def get_str_date(x, offset):
    return f'{x[0]}-{x[1]}-{int(x[2]) - offset}'


def get_timestamp(x):
    return datetime(int(x.tolist()[0]), int(x.tolist()[1]), int(x.tolist()[2])).timestamp()


def parse_data(meteo: DataFrame, hydro: DataFrame) -> list[Series]:
    meteo_offset_file = 'offset_meteo.csv'
    meteo_offset = read_csv(f'data/{meteo_offset_file}', header=None, names=['STATION_NAME', 'OFFSET'])
    meteo_dates = meteo[['YEAR', 'MONTH', 'DAY']].apply(get_timestamp, axis=1)
    hydro_dates = hydro[['YEAR', 'MONTH', 'DAY']].apply(get_timestamp, axis=1)
    meteo['DATE'] = meteo_dates
    hydro['DATE'] = hydro_dates
    hydro['STR_DATA'] = hydro_dates
    meteo_dates = meteo_dates.unique()
    hydro_dates = hydro_dates.unique()

    max_offset = meteo_offset['OFFSET'].max()

    first_date = meteo_dates.min() if meteo_dates.min() > hydro_dates.min() else hydro_dates.min()
    last_date = meteo_dates.max() if meteo_dates.max() < hydro_dates.max() else hydro_dates.max()

    first_date += max_offset * 86400

    water_level_end = hydro[
        (hydro['STATION_NAME'] == 'GŁOGÓW') &
        (hydro['DATE'].ge(first_date)) &
        (hydro['DATE'].le(last_date))
    ]['WATER_LEVEL'].reset_index(drop=True)

    water_level_start = hydro[
        (hydro['STATION_NAME'] == 'RACIBÓRZ-MIEDONIA') &
        (hydro['DATE'].ge(
            first_date - meteo_offset[meteo_offset['STATION_NAME'] == 'RACIBÓRZ-MIEDONIA']['OFFSET'].values[0] * 86400
        )) &
        (hydro['DATE'].le(
            last_date - meteo_offset[meteo_offset['STATION_NAME'] == 'RACIBÓRZ-MIEDONIA']['OFFSET'].values[0] * 86400
        ))
    ]['WATER_LEVEL'].reset_index(drop=True)

    objects = [
        hydro['STR_DATA'],
        water_level_end.rename('WATER_LEVEL_END'),
        water_level_start.rename('WATER_LEVEL_START')
    ]

    for _, station in enumerate(meteo_offset['STATION_NAME']):
        offset = meteo_offset[meteo_offset['STATION_NAME'] == station]['OFFSET'].values[0]
        station_data = meteo[
            (meteo['STATION_NAME'] == station) &
            (meteo['DATE'].ge(first_date - offset * 86400)) &
            (meteo['DATE'].le(last_date - offset * 86400))
        ]['PRECIPITATION'].div(10).reset_index(drop=True)

        if len(station_data) == 0:
            continue

        objects.append(station_data.rename(station))

    return objects


def get_training_data(meteo: DataFrame, hydro: DataFrame) -> DataFrame:
    objects = parse_data(meteo, hydro)

    del objects[0]

    return concat(
        objects,
        axis=1,
        join='inner'
    )


def get_prediction_data(meteo: DataFrame, hydro: DataFrame) -> DataFrame:
    objects = parse_data(meteo, hydro)

    del objects[1]

    return concat(
        objects,
        axis=1,
        join='inner'
    )
