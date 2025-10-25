import flask
import pickle
import pandas
import psycopg2

from flask import request

app = flask.Flask(__name__)
connection = psycopg2.connect(
        host="192.168.8.2",
        port="5432",
        database="barmej",
        user="postgres",
        password="majed"
    ) 

@app.route("/get_data_count", methods=["GET"])
def get_data_count():
    label_name = request.args.get("label_name", type=str)
    count = request.args.get("count", type=int)
    if label_name.lower() not in ["positive", "negative", "neutral"]:
        return f"error '{label_name}' doesn't exists"

    sql = """SELECT lt.label_name
            FROM label_types lt
            JOIN data_labeling dl ON dl.label_id = lt.label_id
            """

    cursor = connection.cursor()
    cursor.execute(sql, (label_name.lower(),))

    results = cursor.fetchall()
    num = 0
    c = 0
    for row in results:
        if num == count:break
        num+=1
        if str(row[0]).lower() == label_name:c+=1
    cursor.close()
    return str(c)

@app.route("/get_data", methods=["GET"])
def get_data():
    sort_order = request.args.get("sort_order", type=str)
    count = request.args.get("count", type=int)
    
    if not sort_order or not count:return "sort_order and count are needed\nsort_order type is string, count type is int"
    if sort_order.lower() not in ['a', 'z']:return "'sort_order' must be 'a' or 'z'"
    
    if sort_order.lower() == 'a':sort = 'ASC'
    if sort_order.lower() == 'z':sort = 'DESC'
    
    sql = f"""SELECT di.txt, lt.label_name
            FROM label_types lt
            JOIN data_labeling dl ON dl.label_id = lt.label_id
            JOIN data_input di ON di.SN = dl.SN
            ORDER BY di.date {sort}
            LIMIT %s;
            """

    cursor = connection.cursor()
    cursor.execute(sql, (count,))
    results = cursor.fetchall()
    return results

# connection.close()
app.run(debug=True)