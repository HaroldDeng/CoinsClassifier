interface MLResult {
    value: number;
}
declare class AJAXAnalysisService {
    readonly canvas: HTMLCanvasElement;
    readonly ctx: CanvasRenderingContext2D;
    query(path: string, method: string | undefined, data: Blob): Promise<XMLHttpRequest>;
    private upload;
    analyze(video: HTMLVideoElement): Promise<MLResult>;
}
declare class WebcamReadyEvent extends Event {
    constructor();
}
declare class Webcam extends EventTarget {
    readonly elem: HTMLVideoElement;
    private stream;
    private images;
    private targetWidth;
    private targetHeight;
    constructor();
    private readonly constraints;
    protected update(): Promise<void>;
    start(): Promise<void>;
    switch(): void;
}
declare class VideoUI {
    readonly canvas: HTMLCanvasElement;
    readonly webcam: Webcam;
    readonly analysis: AJAXAnalysisService;
    private ctx;
    ready: boolean;
    protected nextFrame: number | undefined;
    constructor(canvas: HTMLCanvasElement);
    start(): Promise<void>;
    private onResize;
    private onStream;
    private onTap;
    run: () => void;
    switch(): void;
}
declare const ui: VideoUI;
//# sourceMappingURL=main.d.ts.map