import pandas as pd

class Validations:
    def __init__(self, df:pd.DataFrame, log:object):
        self.log = log
        self.df = df

    def doesnt_pass_data_rules(self) -> None:
        df_filtered = self.df.dropna()
        self.log.warning(f'The rows that have been filtered for data missing are: {pd.concat([self.df ,df_filtered]).drop_duplicates(keep=False)}')
        
    def filtering_data(self) -> pd.DataFrame:
        return self.df.dropna()