import { FlagEvent } from "./FlagEvent";
import { FrontendlibSocket } from "./FrontendlibSocket";
import { FrontendlibSocketIncomingMessage, FrontendlibSocketOutgoingMessage } from "./FrontendlibSocketMessage";


class Frontendlib {
    public readonly socket = new FrontendlibSocket();
    private answerCounter = 0;

    private answerPromises: Record<number, FlagEvent> = {};
    private answers: Record<number, any> = {};

    constructor() {
        this.socket.handlers.push(this.messageHandler);
    }

    private getNextAnswerCounter() {
        let val = this.answerCounter + 1;
        this.answerCounter += 1;
        if (this.answerCounter > 1000000) {
            this.answerCounter = 0;
        }
        return val;
    }

    public async callFunction(functionName: string, ...args: any[]): Promise<any> {
        let answerId = this.getNextAnswerCounter()
        let msg: FrontendlibSocketOutgoingMessage = {
            message_type: "call",
            answer_id: answerId,
            payload: {
                function_name: functionName,
                "args": args
            }
        }
        this.socket.sendMessage(msg);
        let a = this.answerPromises[answerId] = new FlagEvent();
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
            let answerId = message.answer_id as number;
            this.answers[answerId] = message.payload;
            this.answerPromises[answerId].resolve();
        }
        //TODO: other types of messages?
    }
}

window.onload = () => {
    (window as any).frontendlib = new Frontendlib();
};
