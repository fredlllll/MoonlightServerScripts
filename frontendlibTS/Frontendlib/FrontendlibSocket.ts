import { FrontendlibSocketIncomingMessage, FrontendlibSocketOutgoingMessage } from "./FrontendlibSocketMessage";

export class FrontendlibSocket {
    private socket: WebSocket | null = null;
    public readonly handlers: ((socket: FrontendlibSocket, message: FrontendlibSocketIncomingMessage) => void)[] = [];

    public constructor() {
        this.openSocket();
    }

    private openSocket() {
        if (this.socket !== null) {
            this.socket.close();
        }
        this.socket = new WebSocket("ws://" + location.host + "/api/v1/websocket/frontendlib");
        this.socket.addEventListener('close', this.onClose);
        this.socket.addEventListener('error', this.onError);
        this.socket.addEventListener('open', this.onOpen);
        this.socket.addEventListener('message', this.onMessage);
    }

    private onClose = (ev: CloseEvent) => {
        console.log(ev);
        if (ev.code !== 1000) { //dont reopen if we called close (1000)
            this.openSocket();
        }
    }

    private onError = (ev: Event) => {
        console.log(ev);
    }

    private onOpen = () => {
        console.log("websocket opened");
    }

    private onMessage = (ev: MessageEvent) => {
        let msg = JSON.parse(ev.data) as FrontendlibSocketIncomingMessage;
        if (this.handlers) {
            for (var h of this.handlers) {
                try {
                    h(this, msg);
                } catch (error) {
                    console.log(error);
                }
            }
        }
    }

    public sendMessage(message: FrontendlibSocketOutgoingMessage) {
        this.socket?.send(JSON.stringify(message));
    }
}