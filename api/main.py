from fastapi import FastAPI, status, UploadFile, File, HTTPException


from utils import model_management, parse_data, read_files

app = FastAPI()


@app.post('/forecast', status_code=status.HTTP_200_OK, response_model=dict)
async def get_hydro_forecast(hydro_file: UploadFile = File(...), meteo_file: UploadFile = File(...)):
    """
    Get height of Odra river on daily basis based on provided hydrological and meteorological statistic data in files

    :param meteo_file:
    :param hydro_file:
    :return:
    """
    acceptable_content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    if (hydro_file.content_type and meteo_file.content_type) != acceptable_content_type:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'The uploaded file is not in XLSX format')

    filtered_meteo, filtered_hydro = read_files.read_files_prediction(hydro_file, meteo_file)
    data = parse_data.parse_data(filtered_meteo, filtered_hydro)
    data_set_to_prediction = data.to_csv(index=False)
    forecast = model_management.predict_forecast(data_set_to_prediction)
    return forecast
