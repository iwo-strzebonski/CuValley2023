from pandas import DataFrame


def save_data(data: DataFrame, file_name: str) -> None:
    data.to_csv(f'utils/out/{file_name}', index=False)
