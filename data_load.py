import pandas as pd


class Data_Reader():
    """docstring for Read"""

    def __init__(self, filePath="./dataset/Livro1.xlsx"):
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

    def get_df(self):
        return pd.read_excel(self.file_path, engine="openpyxl")

    def get_monthly_precipitation_df(self):
        df = self.get_df()
        df.drop('ano', axis=1, inplace=True)
        return df

    def get_year_idx_df(self):
        df = self.get_df()
        df = df.set_index('ano')
        return df

    def get_years(self):
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
                    'mes': self.months[column] + '-' + str(year),
                    'precipitacao': value[idx]
                })

        df = pd.DataFrame(rows)
        df = df.set_index('mes')
        return df

    def test_training_split(self, dataframe, months_number=12):
        """ Train and Test data Splitting """
        train_data = dataframe.iloc[:months_number]
        test_data = dataframe.iloc[months_number:]
        return {'train': train_data, 'test': test_data}
