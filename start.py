from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from werkzeug.utils import header_property, secure_filename
from export_heatmap import heatmapping
import random

upload_dir = './static/temp/'
allowed_ex = set(['mp4', 'avi', 'mpeg4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_dir
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024      # 8 MB
app.secret_key='lco36d72v6w9d84'


def isallowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_ex


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods = ['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        file = request.files['video_upload']
        if file and isallowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER']+filename)
            session['video']=filename
            return render_template('calibration.html')
        return "File type error."
    return render_template('index.html')


@app.route('/default')
def defaultPlay():
    if 'video' in session:
        session.pop('video',None)
    return render_template('calibration.html')


@app.route('/demo')
def demo():
    if 'video' in session:
        video = session['video']
        session['user'] = str(int(random.random()*1000000))
        return render_template('demo.html', videopath='temp/'+video)
    session['user'] = str(int(random.random()*1000000))
    return render_template('demo.html', videopath='default/IKEA.mp4')


@app.route('/run', methods=['POST'])
def runCV():
    if request.method == "POST":
        pred_data = request.get_json()
        filepath = './static/default/IKEA.mp4' if ('video' not in session) else './static/temp/'+ session['video']
        name = session['user']
        heatmapping(pred_data, filepath, name)

        print(f'User: {name}')
        
        results = {'processed': 'true'}
        return jsonify(results)
    return redirect(url_for('index'))

@app.route('/show')
def wait4video():
    return render_template('waiting.html')


@app.route('/result')
def embedd():
    if 'user' in session:
        name = session['user']
        return render_template('result.html', videopath='res/'+name+'.avi')
    return render_template('result.html', videopath='res/IKEA.mp4')



if __name__ == '__main__':
    app.run(debug=True)