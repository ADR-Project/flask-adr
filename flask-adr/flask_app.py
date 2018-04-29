from flask import Flask, request
from flask import jsonify
from flask import render_template

from utils.drugs import get_drug_details

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html', title='Home')


@app.route("/drug")
def get_do():
    try:
        drug_name = request.args['drug_name']
        temp = request.args['temp']
        pressure = request.args['pressure']
    except KeyError as err:
        d = {
            "status": "error",
            "message": "{field} parameter missing".format(
                field=err.args[0]),
        }
    else:
        result = get_drug_details(
            drug_name=drug_name, temp=temp, pressure=pressure
        )
        if not result:
            d = {
                "status": "error",
                "message": "No drug data found",
            }
        else:
            d = {
                'status': 'SUCCESS',
                'data': result,
            }
    return jsonify(d)


if __name__ == '__main__':
    app.run()
