import { FlagEvent } from "./FlagEvent";
import { FrontendlibSocket } from "./FrontendlibSocket";
import { FrontendlibSocketIncomingMessage, FrontendlibSocketOutgoingMessage } from "./FrontendlibSocketMessage";


export class Frontendlib {
    public readonly socket = new FrontendlibSocket();
    private answerCounter = 0;

    private answerPromises: Record<number, FlagEvent> = {};
    private answers: Record<number, any> = {};
    private channelHandlers: Record<string, ((message: string) => void)[]> = {}

    constructor() {
        this.socket.handlers.push(this.messageHandler);
    }

    private getNextAnswerId() {
        let val = this.answerCounter + 1;
        this.answerCounter += 1;
        if (this.answerCounter > 1000000) {
            this.answerCounter = 0;
        }
        return val;
    }

    public addChannelHandler(channelName: string, func: (message: string) => void): void {
        let handlers = this.channelHandlers[channelName];
        if (handlers === undefined) {
            handlers = this.channelHandlers[channelName] = [];
        }
        handlers.push(func);
        console.log("handler registered for channel " + channelName);
    }

    public removeChannelHandler(channelName: string, func: (message: string) => void): void {
        let handlers = this.channelHandlers[channelName];
        if (handlers === undefined) {
            return;
        }
        let index = handlers.indexOf(func);
        handlers.splice(index, 1);
    }

    public async callFunction(functionName: string, ...args: any[]): Promise<any> {
        let answerId = this.getNextAnswerId()
        let msg: FrontendlibSocketOutgoingMessage = {
            message_type: "call",
            payload: {
                answer_id: answerId,
                function_name: functionName,
                "args": args
            }
        }
        let a = this.answerPromises[answerId] = new FlagEvent();
        this.socket.sendMessage(msg);
        let timeout = setTimeout(() => {
            a.reject();
        }, 1000);
        await a.promise;
        clearTimeout(timeout);
        let answer = this.answers[answerId];
        delete this.answerPromises[answerId];
        delete this.answers[answerId];
        return answer;
    }

    private messageHandler = (socket: FrontendlibSocket, message: FrontendlibSocketIncomingMessage): void => {
        if (message.message_type == "answer") {
            let payload = message.payload;
            let answerId = payload.answer_id as number;
            this.answers[answerId] = payload.result;
            this.answerPromises[answerId].resolve();
        } else if (message.message_type == "exception") {
            //TODO: similar to answer, but make it throw an exception instead of return a result
        } else if (message.message_type == "channel") {
            let payload = message.payload;
            let channel = payload.channel;
            let data = payload.data;
            let handlers = this.channelHandlers[channel];
            if (handlers) {
                for (let handler of handlers) {
                    handler(data)
                }
            }
        }
        //TODO: other types of messages?
    }
}
