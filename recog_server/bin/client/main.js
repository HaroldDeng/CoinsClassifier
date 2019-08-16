"use strict";
class AJAXAnalysisService {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
    }
    query(path, method = 'GET', data) {
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
                }
                else {
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
    async upload(png) {
        const result = await this.query('/api/analysis', 'POST', png);
        const data = result.response;
        console.log(data);
        return data;
    }
    async analyze(video) {
        const { videoWidth: width, videoHeight: height } = video;
        this.canvas.width = width;
        this.canvas.height = height;
        this.ctx.clearRect(0, 0, width, height);
        this.ctx.drawImage(video, 0, 0);
        const png = await new Promise((res, rej) => this.canvas.toBlob(blob => blob == null ? rej() : res(blob), 'image/png'));
        return await this.upload(png);
    }
}
class WebcamReadyEvent extends Event {
    constructor() {
        super('ready', { cancelable: false });
    }
}
class Webcam extends EventTarget {
    constructor() {
        super();
        this.elem = document.createElement('video');
        this.targetWidth = -1;
        this.targetHeight = -1;
        this.elem.setAttribute('autoplay', true);
    }
    get constraints() {
        const result = {};
        if (this.targetWidth > 0)
            result.width = { ideal: this.targetWidth };
        if (this.targetHeight > 0)
            result.height = { ideal: this.targetHeight };
        return result;
    }
    async update() {
        const stream = this.stream;
        if (stream == undefined)
            return;
        const track = stream.getVideoTracks()[0];
        await track.applyConstraints(this.constraints);
    }
    async start() {
        this.stream = await navigator.mediaDevices.getUserMedia({ video: this.constraints, audio: false });
        console.log("Got stream", this.stream);
        this.elem.srcObject = this.stream;
        const track = this.stream.getTracks()[0];
        this.dispatchEvent(new WebcamReadyEvent());
    }
    switch() {
        this.elem.pause();
        this.elem.srcObject = null;
    }
}
class VideoUI {
    constructor(canvas) {
        this.canvas = canvas;
        this.webcam = new Webcam();
        this.analysis = new AJAXAnalysisService();
        this.ready = false;
        this.onResize = () => {
            const { width, height } = this.canvas.getBoundingClientRect();
            this.canvas.width = width;
            this.canvas.height = height;
        };
        this.onStream = () => {
            this.ctx = this.canvas.getContext('2d');
            if (this.nextFrame == undefined)
                this.run();
        };
        this.onTap = async () => {
            if (!this.ready)
                return;
            if (this.webcam.elem.paused) {
                this.webcam.elem.play();
                return;
            }
            this.webcam.elem.pause();
            const data = await this.analysis.analyze(this.webcam.elem);
            alert(`You have ${(data.value / 100).toFixed(2)}`);
            this.webcam.elem.play();
        };
        this.run = () => {
            const ctx = this.ctx;
            ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            ctx.drawImage(this.webcam.elem, 0, 0);
            this.nextFrame = requestAnimationFrame(this.run);
        };
        this.webcam.addEventListener('ready', this.onStream);
        window.addEventListener('resize', this.onResize);
        canvas.addEventListener('click', this.onTap);
    }
    async start() {
        this.onResize();
        await this.webcam.start();
        this.ready = true;
    }
    switch() {
        this.webcam.switch();
    }
}
const ui = new VideoUI(document.querySelector('canvas'));
ui.start();
//# sourceMappingURL=main.js.map