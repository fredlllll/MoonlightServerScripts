System.register("FlagEvent", [], function (exports_1, context_1) {
    "use strict";
    var FlagEvent, c;
    var __moduleName = context_1 && context_1.id;
    return {
        setters: [],
        execute: function () {
            FlagEvent = class FlagEvent {
                constructor() {
                    this.resolve = () => {
                        this.promResolve();
                    };
                    this.reject = () => {
                        this.promReject();
                    };
                    this.prom = new Promise((res, rej) => {
                        this.promResolve = res;
                        this.promReject = rej;
                    });
                }
                get promise() {
                    return this.prom;
                }
            };
            exports_1("FlagEvent", FlagEvent);
        }
    };
});
System.register("FrontendlibSocketMessage", [], function (exports_2, context_2) {
    "use strict";
    var __moduleName = context_2 && context_2.id;
    return {
        setters: [],
        execute: function () {
        }
    };
});
System.register("FrontendlibSocket", [], function (exports_3, context_3) {
    "use strict";
    var FrontendlibSocket;
    var __moduleName = context_3 && context_3.id;
    return {
        setters: [],
        execute: function () {
            FrontendlibSocket = class FrontendlibSocket {
                constructor() {
                    this.socket = null;
                    this.handlers = [];
                    this.onClose = (ev) => {
                        console.log(ev);
                        if (ev.code !== 1000) { //dont reopen if we called close (1000)
                            this.openSocket();
                        }
                    };
                    this.onError = (ev) => {
                        console.log(ev);
                    };
                    this.onOpen = () => {
                        console.log("websocket opened");
                    };
                    this.onMessage = (ev) => {
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
                sendMessage(message) {
                    var _a;
                    (_a = this.socket) === null || _a === void 0 ? void 0 : _a.send(JSON.stringify(message));
                }
            };
            exports_3("FrontendlibSocket", FrontendlibSocket);
        }
    };
});
System.register("Frontendlib", ["FlagEvent", "FrontendlibSocket"], function (exports_4, context_4) {
    "use strict";
    var FlagEvent_1, FrontendlibSocket_1, Frontendlib;
    var __moduleName = context_4 && context_4.id;
    return {
        setters: [
            function (FlagEvent_1_1) {
                FlagEvent_1 = FlagEvent_1_1;
            },
            function (FrontendlibSocket_1_1) {
                FrontendlibSocket_1 = FrontendlibSocket_1_1;
            }
        ],
        execute: function () {
            Frontendlib = class Frontendlib {
                constructor() {
                    this.socket = new FrontendlibSocket_1.FrontendlibSocket();
                    this.answerCounter = 0;
                    this.answerPromises = {};
                    this.answers = {};
                    this.channelHandlers = {};
                    this.messageHandler = (socket, message) => {
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
                    let a = this.answerPromises[answerId] = new FlagEvent_1.FlagEvent();
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
            };
            exports_4("Frontendlib", Frontendlib);
        }
    };
});
//# sourceMappingURL=frontendlib.js.map