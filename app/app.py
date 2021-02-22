from flask import Flask, render_template, request, flash, redirect, url_for, Response
from werkzeug.utils import secure_filename
import librosa
from scipy.signal import find_peaks
import pandas as pd
import os

if not os.path.exists('temp_audio_dir'):
    os.makedirs('temp_audio_dir')

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = os.urandom(12).hex()
app.config['UPLOAD_FOLDER'] = 'temp_audio_dir'


VALID_EXTENSIONS = {'wav', 'mp3', 'm4a', 'aac', 'ogg', 'oga', 'flac'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in VALID_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('detect_coughs',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload Sound File</title>
    <h1>Upload Audio File for Detecting Coughs</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Detect>
    </form>
    '''


@app.route('/detect_coughs', methods=['GET', 'POST'])
def detect_coughs():
    if request.args.get('filename', None) is None or '':
        if request.files.get('file', None) is None or '':
            return Response("Bad request", 400)
        else:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return get_cough_timings(filename)
            else:
                return Response("Bad file request", 400)
    else:
        return get_cough_timings(request.args['filename'])


def get_cough_timings(filename):
    if filename is not None:
        audio, sr = librosa.load(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))

        # We take audio samples who have a minimum amplitude of 0.275 and there's a prominence of 1.2
        # under 3 second window so as we get the peakest point of cough
        peak_indices, _ = find_peaks(audio, height=(
            0.275, None), prominence=1.15, distance=3*sr)

        # Get the timestamps relative to sample indices
        peaks = peak_indices / sr

        out = pd.DataFrame({'peak_start': peaks})

        proper_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(proper_path):
            os.remove(proper_path)

        return Response(out.to_json(), mimetype='application/json')


@app.errorhandler(413)
def error413(e):
    return render_template('413.html')


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
