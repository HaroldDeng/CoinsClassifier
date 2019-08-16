interface MLResult {
	value: number;
}

class AJAXAnalysisService {
	readonly canvas = document.createElement('canvas');
	readonly ctx = this.canvas.getContext('2d')!;
	
	query(path: string, method: string = 'GET', data: Blob): Promise<XMLHttpRequest> {
		// Create the XHR request
		var request = new XMLHttpRequest();
		request.responseType = 'json';

		// Return it as a Promise
		return new Promise((resolve, reject) => {
			// Setup our listener to process compeleted requests
			request.addEventListener('readystatechange', () => {
				// Only run if the request is complete
				if (request.readyState !== 4)
					return;
				
				// Process the response
				if (request.status >= 200 && request.status < 300) {
					// If successful
					resolve(request);
				} else {
					// If failed
					reject({
						status: request.status,
						statusText: request.statusText
					});
				}
			});

			// Setup our HTTP request
			request.open(method, path, true);

			// Send the request
			const form = new FormData();
			form.append('image', data, 'blob');
			request.send(form);
		});
	}
	private async upload(png: Blob): Promise<MLResult> {
		const result = await this.query('/api/analysis', 'POST', png);
		const data = result.response;
		console.log(data);
		return data;
	}
	async analyze(video: HTMLVideoElement): Promise<MLResult> {
		const { videoWidth: width, videoHeight: height } = video;
		this.canvas.width = width;
		this.canvas.height = height;
		this.ctx.clearRect(0, 0, width, height);
		this.ctx.drawImage(video, 0, 0);
		const png = await new Promise<Blob>((res, rej) =>
				this.canvas.toBlob(blob => blob == null ? rej() : res(blob), 'image/png'));
		return await this.upload(png);
	}
}