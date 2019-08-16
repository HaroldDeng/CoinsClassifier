class WebcamReadyEvent extends Event {
    constructor() {
        super('ready', { cancelable: false });
    }
}

class Webcam extends EventTarget{
    readonly elem = document.createElement('video');
    private stream: MediaStream | undefined;
    private targetWidth: number = -1;
    private targetHeight: number = -1;
    constructor() {
        super();
        this.elem.setAttribute('autoplay', true as any);
    }
    private get constraints(): MediaTrackConstraints {
        const result: MediaTrackConstraints = { };
        if (this.targetWidth > 0)
            result.width = { ideal: this.targetWidth };
        if (this.targetHeight > 0)
            result.height = { ideal: this.targetHeight };
        return result;
    }
    protected async update() {
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
    readonly webcam = new Webcam();
    readonly analysis = new AJAXAnalysisService();
    private ctx: CanvasRenderingContext2D | undefined;
    ready: boolean = false;

    protected nextFrame: number | undefined;

    constructor(readonly canvas: HTMLCanvasElement) {
        this.webcam.addEventListener('ready', this.onStream);
        window.addEventListener('resize', this.onResize);
        canvas.addEventListener('click', this.onTap);
    }
    async start() {
        this.onResize();
        await this.webcam.start();
        this.ready = true;
    }
    private onResize = () => {
        const { width, height } = this.canvas.getBoundingClientRect();
        this.canvas.width = width;
        this.canvas.height = height;
    }
    private onStream = () => {
        this.ctx = this.canvas.getContext('2d')!;
        if (this.nextFrame == undefined)
            this.run();
    }
    private onTap = async () => {
        if (!this.ready)
            return;
        
        if (this.webcam.elem.paused) {
            this.webcam.elem.play();
            return;
        }

        this.webcam.elem.pause();
        const data = await this.analysis.analyze(this.webcam.elem);
    }
    run = () => {
        const ctx = this.ctx!;
        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        ctx.drawImage(this.webcam.elem, 0, 0);
        this.nextFrame = requestAnimationFrame(this.run)
    }
    switch() {
        this.webcam.switch();
    }
}

const ui = new VideoUI(document.querySelector('canvas')!);
ui.start();