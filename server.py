import flask
import psycopg2.extras
from flask import render_template, request, redirect
from utils import translate

conn_string_local = "host='127.0.0.1' dbname='reestri' user='postgres' password=''"

connection = psycopg2.connect(conn_string_local)
cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

SELECT_CONSTANT = """
            select personal_number, first_name, last_name, fathers_name, dob, 
            case when sex=1 then 'Male' when sex=2 then 'Female' else '' end as sex, 
            street || COALESCE(', ' || district, '') as address from persons
"""


@app.route("/")
def index():
    return redirect("/page/")


@app.route("/page/", methods=['GET'], defaults={'page': 1})
@app.route("/page/<page>", methods=['GET'])
def home(page):
    rows_per_page = 100
    page = int(page)
    cursor.execute(f"""{SELECT_CONSTANT} limit {rows_per_page * page} offset {rows_per_page * (page - 1)};""")
    result_list = translate(data=cursor.fetchall(), to='ka',
                            fields=['first_name', 'last_name', 'fathers_name', 'address'])
    return render_template('home.html', data_list=result_list)


@app.route("/search", methods=["POST"])
def search():
    non_null_parameters = []
    for k, v in request.form.items():
        if v != '':
            non_null_parameters.append([k, v])
    non_null_parameters = translate(data=non_null_parameters, to='latin',
                                    fields=['first_name', 'last_name', 'fathers_name', 'address'])
    print(non_null_parameters)
    iterable = iter(non_null_parameters)
    first_param = next(iterable)
    query = f"{SELECT_CONSTANT} where {first_param[0]} ilike '%{first_param[1]}%'"
    for k, v in iterable:
        if v != '':
            query += f" and {k} ilike '%{v}%'"
    query += ";"
    cursor.execute(query)
    result_list = translate(data=cursor.fetchall(), to='ka',
                            fields=['first_name', 'last_name', 'fathers_name', 'address'])
    return render_template('home.html', data_list=result_list)


app.run(host='127.0.0.1', port=8080)

connection.close()
