import pandas as pd


def read_data(file_path: str) -> pd.DataFrame:
    """
    Читает данные из CSV-файла.
    """
    df = pd.read_csv(file_path, delimiter=';')
    df['Дата'] = pd.to_datetime(df['Дата'])
    return df

def sort_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Сортирует данные по дате.
    """
    return df.sort_values(by='Дата')

def group_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Группирует данные по программе выпечки и номеру духовки.
    """
    return df.groupby(['Программа', 'Номер духовки'])

def write_data(df: pd.DataFrame, file_path: str):
    """
    Записывает данные в CSV-файл.
    """
    df.to_csv(file_path, sep=';', index=False)
