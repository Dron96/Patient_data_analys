from api import app
from api import algo_func as a
from io import BytesIO
from flask import send_file


@app.route('/api/exam/<int:exam_id>', methods=['GET'])
def get_examination(exam_id):
    df = a.get_exam_data(exam_id)
    return df.to_html()


@app.route('/api/exam/<int:exam_id>/desc', methods=['GET'])
def get_description(exam_id):
    total = a.get_description_data(exam_id)
    return total.to_html(classes='table table-hover')


@app.route('/api/exam/<int:exam_id>/graph', methods=['GET'])
def get_graph(exam_id):
    plt = a.get_graph(exam_id)

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')
