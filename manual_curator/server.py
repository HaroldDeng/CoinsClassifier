import argparse
from flask import Flask, request, send_from_directory
from db import ImageDB


parser = argparse.ArgumentParser()
parser.add_argument('--db', default='labels.json', help='database path', type=str)
parser.add_argument('-p', '--port', default=8080, help='port to start server on', type=int)
parser.add_argument('--images', default='./images', help='image directory', type=str)
args = parser.parse_args()

print(f'Loading/creating database from {args.db}')
db = ImageDB(args.db, args.images)


app = Flask(__name__, static_url_path='')


@app.route('/')
def serve_index():
	return send_from_directory('.', 'index.html')


@app.route('/js/<path:path>')
def serve_js(path):
	return send_from_directory('./js', path)


@app.route('/img/<path:path>')
def serve_image(path):
	return send_from_directory(args.images, path)


@app.route('/api/nextimg')
def serve_next_image():
	print('Finding image')
	image = next(db, '')
	return image


@app.route('/api/label', methods=['POST'])
def recieve_label():
	json = request.get_json(silent=True)
	print(json)
	name = json['name']
	t = json['type']
	f = json['face']
	u = json['user']
	print(f'Classified {name} as {t} {f} by {u}')
	db.label(name, t, f, u)
	return serve_next_image()


if __name__ == "__main__":
	app.run()
