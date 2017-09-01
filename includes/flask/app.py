from flask import Flask
from flask import render_template
from flask import request
import urllib
from subprocess import call

import json

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def work_it():
    uri = request.form['uri']

    print(request.form)
    if uri:
        print('downloading uri {0}'.format(uri))
        try:
            urllib.urlretrieve(uri, '/work/flask/static/top.jpg')
        except:
            return json.dumps({'ret': 'False',
                               'msg': 'could not download {0}'.format(uri)})

        try:
            call(['bash', '/work/flask/doit.sh'])
            return json.dumps({'ret': 'True',
                               'topImage': '/static/top.jpg',
                               'bottomImage': '/static/bottom.bmp',
                               'msg': 'success'})
        except:
            return json.dumps({'ret': 'False',
                               'msg': 'failure running back end process'})
    else:
        return json.dumps(
            {'ret': 'False', 'msg': 'include a url for download'})


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers[
        "Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

if __name__ == "__main__":
    app.run(host='0.0.0.0')
