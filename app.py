from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as sql
import pandas as pd


app = Flask(__name__)

# tworzymy polaczenie z baza - jesli nie istnieje zostanie utworzona
conn = sql.connect('instance/dane_db.sqlite', check_same_thread=False)
cur = conn.cursor()
# sprawdzamy czy w bazie istenieje tabela dane jesli nie - tworzymy tabele i ladujemy dane
try:
    cur.execute('select count(*) from dane')
    print('Tabela z danymi istnieje')
except sql.OperationalError as e:
    if e.args[0].startswith('no such table'):
        print('Tabela z danymi nie istnieje - tworzę')
        df = pd.read_csv('csv1.csv',
                         sep=',',
                         encoding="UTF-8",
                         skiprows=[1],
                         dtype={'Salaries Reported': 'int64', 'Salary': 'float64'},
                         usecols=['Nrow', 'Company Name', 'Job Title', 'Salaries Reported', 'Location', 'Salary']
                         )
        df.to_sql('dane', conn, if_exists="replace")
    else:
        print(e)


# obsluga strony w przegladarce
@ app.route('/')
def str_glowna():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def pobierz():
    city = request.form.get('miasto')
    oper = request.form.get('Operacja')
    dane_sr = []
    dane_mx = []
    dane_re = []
    if oper == 'Odczyt':
        dane_sr.clear()
        dane_mx.clear()
        dane_re.clear()
        # wyliczamy srednie wynagrodzenie dla stanowiska w danej lokalizacji sortujemy od najwyzszego
        zap_sr = (f'SELECT "Location", "Job Title", '
                  f'(ROUND(SUM("Salary" * ("Salaries Reported"))/(SUM("Salaries Reported")),1)) AS "Avg_sal" '
                  f'FROM dane WHERE "Location" = "{city}" GROUP BY "Location", "Job Title" ORDER BY 3 DESC ')
        for row in cur.execute(zap_sr):
            row = list(row)
            dane_sr.append(row)
        # obliczamy rekomendacje - wskazanie najbardziej oplacalnego stanowiska w danej firmie
        zap_re = (f'SELECT tb."Company Name", tb."Job Title", MAX(tb."Avg_sal") AS Max_sal '
                  f'FROM (SELECT "Company Name", "Job Title", ROUND(("Salary")/("Salaries Reported"), 1) AS "Avg_sal" '
                  f'FROM dane WHERE "Location" = "{city}") AS tb GROUP BY tb."Company Name" ORDER BY 1, 3 DESC')
        for row in cur.execute(zap_re):
            row = list(row)
            dane_re.append(row)
        # obliczamy 3 najlepiej placace firmy w danej lokalizacji
        zap_mx = (f'SELECT tba."Company Name", tba."Job Title", tba."Sal_mx" , '
                  f'ROUND(((tba."Sal_mx"/tbb."Sal_avg")-1) * 100) AS "Proc" FROM '
                  f'(SELECT "Location", "Company Name", "Job Title", MAX(ROUND(("Salary"), 1)) AS "Sal_mx" FROM '
                  f'dane WHERE "Location" = "{city}" GROUP BY "Location", "Company Name","Job Title" '
                  f'ORDER BY 4 DESC LIMIT 3) AS tba, (SELECT "Location","Job Title", '
                  f'(ROUND(SUM("Salary" * ("Salaries Reported"))/(SUM("Salaries Reported")),1)) AS "Sal_avg" FROM '
                  f'dane WHERE "Location" = "{city}" GROUP BY "Location", "Job Title" ORDER BY 3 DESC) AS tbb '
                  f'WHERE tba."Location" = tbb."Location" AND tba."Job Title" = tbb."Job Title"')
        for row in cur.execute(zap_mx):
            row = list(row)
            dane_mx.append(row)
    # czyscimy dane
    elif oper == "Czysc":
        dane_sr.clear()
        dane_mx.clear()
        dane_re.clear()
        city = ''
    elif oper == "Koniec":
        quit()
    return render_template('index.html', miasto=city, dane_sr=dane_sr, dane_re=dane_re, dane_mx=dane_mx)


if __name__ == "__main__":
    app.run()
