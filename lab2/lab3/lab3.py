from spyre import server
import pandas as pd
import os

class StockExample(server.App):
    title = "NOAA data visualization"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'NOAA data dropdown', 
            "options": [
                {"label": "VCI", "value": "VCI"}, 
                {"label": "TCI", "value": "TCI"}, 
                {"label": "VHI", "value": "VHI"}
            ], 
            "key": 'ticker', 
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Area',
            "options": [
                {"label": "Вінницька", "value": "Вінницька"},
                {"label": "Волинська", "value": "Волинська"},
                {"label": "Дніпропетровська", "value": "Дніпропетровська"},
                {"label": "Донецька", "value": "Донецька"},
                {"label": "Житомирська", "value": "Житомирська"},
                {"label": "Закарпатська", "value": "Закарпатська"},
                {"label": "Запорізька", "value": "Запорізька"},
                {"label": "Івано-Франківська", "value": "Івано-Франківська"},
                {"label": "Київська", "value": "Київська"},
                {"label": "Кіровоградська", "value": "Кіровоградська"},
                {"label": "Луганська", "value": "Луганська"},
                {"label": "Львівська", "value": "Львівська"},
                {"label": "Миколаївська", "value": "Миколаївська"},
                {"label": "Одеська", "value": "Одеська"},
                {"label": "Полтавська", "value": "Полтавська"},
                {"label": "Рівенська", "value": "Рівенська"},
                {"label": "Сумська", "value": "Сумська"},
                {"label": "Тернопільська", "value": "Тернопільська"},
                {"label": "Харківська", "value": "Харківська"},
                {"label": "Херсонська", "value": "Херсонська"},
                {"label": "Хмельницька", "value": "Хмельницька"},
                {"label": "Черкаська", "value": "Черкаська"},
                {"label": "Чернівецька", "value": "Чернівецька"},
                {"label": "Чернігівська", "value": "Чернігівська"},
                {"label": "Республіка Крим", "value": "Республіка Крим"},
                {"label": "Київ", "value": "Київ"},
                {"label": "Севастополь", "value": "Севастополь"}
            ],
            "key": 'Area',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Year', 
            "key": 'Year', 
            "value": "1985",
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Weeks ranges', 
            "key": 'week_range', 
            "value": "1-10",
            "action_id": "update_data"
        }
    ]

    controls = [{"type": "hidden",
                 "id": "update_data"}]
    
    tabs = ["Plot", "Table"]


    outputs = [
        {
            "type":"plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type":"table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]
    def getData(self, params):
        selected_column = params['ticker']
        start_week, end_week = map(int, params['week_range'].split('-'))
        plot_data = df[(df["area"] == params['Area']) & 
                   (df["Year"] == int(params['Year'])) & 
                   (df["Week"].between(start_week, end_week))]
        plot_data = plot_data[['Year', 'Week', selected_column, 'area']]
        return plot_data


    def getPlot(self, params):
        selected_column = params['ticker']
        plot_data = self.getData(params)
        plot = plot_data.plot(x='Week', y=selected_column)
        fig = plot.get_figure()
        return fig

directory = 'E:/2 курс/2 семестр/Підготовка та аналіз даних/lab2/files'

def read_files(directory):
  files = os.listdir(directory)
  headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
  data_frame = pd.DataFrame()
  for i in range(len(files)):
    file_path = os.path.join(directory, files[i])
    df = pd.read_csv(file_path, header = 1, names = headers)
    df = df.drop('empty', axis=1)
    df = df.drop(df.loc[df['VHI'] == -1].index)
    df['area'] = i+1
    df['Year'] = df['Year'].str.replace('<tt><pre>', '')
    df = df.drop(df[df['Year'] == '</pre></tt>'].index)
    df["Year"] = df["Year"].astype(int)
    data_frame = pd.concat([data_frame, df])
    
  data_frame=data_frame.reset_index(drop=True) 
  return data_frame

def rename_region(df):
  names =  {1: "Вінницька", 2: "Волинська", 3: "Дніпропетровська", 4: "Донецька", 5: "Житомирська", 6: "Закарпатська", 7: "Запорізька", 8: "Івано-Франківська", 9: "Київська", 10: "Кіровоградська", 11: "Луганська", 12: "Львівська", 13: "Миколаївська", 14: "Одеська", 15: "Полтавська", 16: "Рівенська", 17: "Сумська", 18: "Тернопільська", 19: "Харківська", 20: "Херсонська", 21: "Хмельницька", 22: "Черкаська", 23: "Чернівецька", 24: "Чернігівська", 25: "Республіка Крим", 26: "Київ", 27: "Севастопіль"}
 
  for name in names:
    df["area"] = df["area"].replace({name:names[name]})
  return df

df = rename_region(read_files(directory))
print(df)
app = StockExample()
app.launch(port=8080)

