from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

df = pd.read_csv(filepath_or_buffer='D:\Project Data\API\stations.txt', sep=',', skiprows=17)
stations = df[['STAID', 'STANAME                                 ']]


@app.route("/")
def home():
    return render_template('home.html', data=stations.to_html())


@app.route('/api/v1/<station>/<date>')
def about(station, date):

    filepath = f"D:/Project Data/API/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filepath_or_buffer=filepath, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze()/10

    return {'station': station,
            'date': date,
            'temperature': temperature
            }


@app.route('/api/v1/<station>')
def all_about(station):

    filepath = f"D:/Project Data/API/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filepath_or_buffer=filepath, skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient="records")
    return result


@app.route('/api/v1/yearly/<station>/<year>')
def all_about_year(station,year):

    filepath = f"D:/Project Data/API/TG_STAID{str(station).zfill(6)}.txt"
    df = pd.read_csv(filepath_or_buffer=filepath, skiprows=20)
    df['    DATE']=df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient='records')
    return result


if __name__ == '__main__':
    app.run(load_dotenv=True)
