class AnalysisService extends EventTarget {
    private readonly socket: WebSocket;
    constructor() {
        super();
        this.socket = new WebSocket(`ws://${window.location.host}/api/echo`, ["coinv1"]);
        this.socket.addEventListener('open', this.onOpen);
        this.socket.addEventListener('message', this.onMessage);
    }
    private onOpen = (e: Event) => {
        console.log(this.socket, e);
    }
    private onMessage = (e: MessageEvent) => {
        console.log(e);
    }
}
(window as any)['Ana'] = AnalysisService;