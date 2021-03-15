from api import app
from flask import jsonify
import psycopg2


@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/api', methods=['GET'])
def get_all_users():
    conn = psycopg2.connect(
        dbname='spiral',
        user='dron',
        host='127.0.0.1',
        port='5432')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    records = cursor.fetchall()

    return jsonify(records)


@app.route('/api/patient/', methods=['GET'])
def get_all_patients():
    # return 'User %d' % user_id
    conn = psycopg2.connect(
        dbname='spiral',
        user='dron',
        host='127.0.0.1',
        port='5432')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients')
    records = cursor.fetchall()
    return jsonify(records)


@app.route('/api/patient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    # return 'User %d' % user_id
    conn = psycopg2.connect(
        dbname='spiral',
        user='dron',
        host='127.0.0.1',
        port='5432')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients WHERE id = {}'.format(patient_id))
    records = cursor.fetchall()
    return jsonify(records)
