import pandas as pd


class Data_Reader():
    """docstring for Read"""

    def __init__(self, filePath="./dataset/Registo_anual_chuva_marco_2022.xlsx"):
        self.file_path = filePath
        self.months = {
            'janeiro': '01',
            'fevereiro': '02',
            'março': '03',
            'abril': '04',
            'maio': '05',
            'junho': '06',
            'julho': '07',
            'agosto': '08',
            'setembro': '09',
            'outubro': '10',
            'novembro': '11',
            'dezembro': '12'
        }

    def get_filePath(self):
        return self.file_path

    def set_filePath(self, filePath):
        self.file_path = filePath

    def data_size(self):
        pass

    def get_df(self):
        """ read file and remove uncessery data """
        df = pd.read_excel(self.file_path, engine="openpyxl", parse_dates=True)
        df.drop(['total', 'Ano Hidrológico'], axis=1, inplace=True)
        # Dropping last 4 rows using drop: blank space, avg, max and min rows
        df.drop(df.tail(4).index, inplace=True)
        return df

    def get_monthly_precipitation_df(self):
        """ monthly precipitation dataframe """
        df = self.get_df()
        df.drop('ano', axis=1, inplace=True)
        return df

    def get_year_idx_df(self):
        """ """
        df = self.get_df()
        df = df.set_index('ano')
        return df

    def get_years(self):
        """ """
        return self.get_df()['ano']

    def transform(self):
        years = self.get_years()
        monthly_precip = self.get_monthly_precipitation_df()

        rows = []
        for idx in years.index:
            year = years[idx]
            for column, value in monthly_precip.iteritems():
                # print(months[column] + '-' + str(year), value[idx])
                rows.append({
                    'mes': pd.to_datetime(str(year) + '-' + self.months[column] + '-01', format='%Y-%m-%d'),  # self.months[column] + '-' + str(year),
                    'precipitacao': value[idx]
                })

        df = pd.DataFrame(rows)
        df = df.set_index('mes')
        return df

    def test_training_split(self, dataframe, months_test_size=24):
        """ Train and Test data Splitting """
        data_size = dataframe.shape[0]
        train_data = dataframe.iloc[:(data_size - months_test_size)]
        test_data = dataframe.iloc[(data_size - months_test_size):]
        return {'train': train_data, 'test': test_data}
