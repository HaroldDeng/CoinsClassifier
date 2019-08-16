import argparse
from flask import Flask, request, send_from_directory
from circle_in import crop_circles
import test_web as tw
import cv2
import numpy as np
import shutil
import os

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
	blob.save('./upload.png')
	image = cv2.imread('./upload.png')
	os.remove('./upload.png')

	frames = []
	try:
		os.mkdir('./tmp')
		os.mkdir('./tmp/tmp')
	except OSError:
		pass
	
	def write_callback(frame, i, x, y, r, **kwargs):
		#result.append({'x': x, 'y': y, 'width': r, 'height': r, })
		fname = dst.format_map({'src': src, 'i': i, 'x': x, 'y': y, 'r': r, 'radius': r})
		cv2.imwrite(frame, './tmp/tmp/gen_{}.jpg'.format(i))
	crop_circles(image, write_callback)
	cents = tw.main('./tmp')
	shutil.rmtree('./tmp', ignore_errors=True)
	return '{"value":{}}'.format(cents), 200, { 'Content-type': 'application/json' }


if __name__ == "__main__":
	app.run()
