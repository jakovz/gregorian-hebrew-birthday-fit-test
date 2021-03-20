from flask import Flask, render_template, request
from pyluach import dates
import datetime

app = Flask(__name__)
YEARS_TO_CHECK = 100


@app.route('/gregorian_years')
def iteryears():
    if not request.args['date']:
        return render_template('years_viewer.html', hebrew_date='', years_list=[])
    date = datetime.datetime.strptime(request.args['date'], '%Y-%m-%d')
    gregorian_date = dates.GregorianDate(date.year, date.month, date.day)
    hebrew_date: dates.HebrewDate = gregorian_date.to_heb()
    years = []
    for i in range(dates.GregorianDate.today().year, dates.GregorianDate.today().year + YEARS_TO_CHECK):
        georgian_new_date = dates.GregorianDate(i, gregorian_date.month, gregorian_date.day)
        gregorian_hebrew_date = georgian_new_date.to_heb()
        if gregorian_hebrew_date.month == hebrew_date.month and gregorian_hebrew_date.day == hebrew_date.day:
            years.append(i)
    return render_template('years_viewer.html', hebrew_date=hebrew_date, years_list=years)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.args:
        return iteryears()
    return render_template('main.html', years_list=[])


if __name__ == '__main__':
    app.run()
