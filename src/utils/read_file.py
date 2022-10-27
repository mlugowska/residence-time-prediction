import pandas as pd

from utils import externals


def read_excel(sheet_name: str) -> pd.DataFrame:
    return pd.read_excel(f'{externals.DATA_PATH}/complex-data-progress.xlsx', sheet_name=sheet_name)
