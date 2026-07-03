export class FrontendlibSocket {
    socket = null;
    handlers = [];
    constructor() {
        this.openSocket();
    }
    openSocket() {
        if (this.socket !== null) {
            this.socket.close();
        }
        this.socket = new WebSocket("ws://" + location.host + "/api/v1/websocket/frontendlib");
        this.socket.addEventListener('close', this.onClose);
        this.socket.addEventListener('error', this.onError);
        this.socket.addEventListener('open', this.onOpen);
        this.socket.addEventListener('message', this.onMessage);
    }
    onClose = (ev) => {
        console.log(ev);
        if (ev.code !== 1000) { //dont reopen if we called close (1000)
            this.openSocket();
        }
    };
    onError = (ev) => {
        console.log(ev);
    };
    onOpen = () => {
        console.log("websocket opened");
    };
    onMessage = (ev) => {
        let msg = JSON.parse(ev.data);
        if (this.handlers) {
            for (var h of this.handlers) {
                try {
                    h(this, msg);
                }
                catch (error) {
                    console.log(error);
                }
            }
        }
    };
    sendMessage(message) {
        this.socket?.send(JSON.stringify(message));
    }
}
//# sourceMappingURL=FrontendlibSocket.js.map