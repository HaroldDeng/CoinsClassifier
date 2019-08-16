import argparse
from flask import Flask, request, send_from_directory


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=8080, help='port to start server on', type=int)
args = parser.parse_args()


app = Flask(__name__, static_url_path='')


@app.route('/')
def serve_index():
	return send_from_directory('./static', 'index.html')


@app.route('/js/<path:path>')
def serve_js(path):
	return send_from_directory('./bin/client', path)


@app.route('/img/<path:path>')
def serve_image(path):
	return send_from_directory(args.images, path)


@app.route('/api/analysis', methods=['GET','POST'])
def analyze_image():
	print('0')
	blob = request.files['image']
	print('a')
	print(blob)
	return '[]', 200, { 'Content-type': 'application/json' }


if __name__ == "__main__":
	app.run()
