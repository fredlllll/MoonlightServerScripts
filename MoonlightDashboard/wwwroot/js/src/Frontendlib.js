import { FlagEvent } from "./FlagEvent";
import { FrontendlibSocket } from "./FrontendlibSocket";
export class Frontendlib {
    socket = new FrontendlibSocket();
    answerCounter = 0;
    answerPromises = {};
    answers = {};
    channelHandlers = {};
    constructor() {
        this.socket.handlers.push(this.messageHandler);
    }
    getNextAnswerId() {
        let val = this.answerCounter + 1;
        this.answerCounter += 1;
        if (this.answerCounter > 1000000) {
            this.answerCounter = 0;
        }
        return val;
    }
    addChannelHandler(channelName, func) {
        let handlers = this.channelHandlers[channelName];
        if (handlers === undefined) {
            handlers = this.channelHandlers[channelName] = [];
        }
        handlers.push(func);
        console.log("handler registered for channel " + channelName);
    }
    removeChannelHandler(channelName, func) {
        let handlers = this.channelHandlers[channelName];
        if (handlers === undefined) {
            return;
        }
        let index = handlers.indexOf(func);
        handlers.splice(index, 1);
    }
    async callFunction(functionName, ...args) {
        let answerId = this.getNextAnswerId();
        let msg = {
            message_type: "call",
            payload: {
                answer_id: answerId,
                function_name: functionName,
                "args": args
            }
        };
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
    messageHandler = (socket, message) => {
        if (message.message_type == "answer") {
            let payload = message.payload;
            let answerId = payload.answer_id;
            this.answers[answerId] = payload.result;
            this.answerPromises[answerId].resolve();
        }
        else if (message.message_type == "exception") {
            //TODO: similar to answer, but make it throw an exception instead of return a result
        }
        else if (message.message_type == "channel") {
            let payload = message.payload;
            let channel = payload.channel;
            let data = payload.data;
            let handlers = this.channelHandlers[channel];
            if (handlers) {
                for (let handler of handlers) {
                    handler(data);
                }
            }
        }
        //TODO: other types of messages?
    };
}
//# sourceMappingURL=Frontendlib.js.map