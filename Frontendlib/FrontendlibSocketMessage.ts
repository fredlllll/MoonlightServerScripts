type messageTypeIncoming = "answer" | "exception" | "channel";
type messageTypeOutgoing = "call";

export interface FrontendlibSocketIncomingMessage {
    message_type: messageTypeIncoming;
    payload: any;
}

export interface FrontendlibSocketOutgoingMessage {
    message_type: messageTypeOutgoing;
    payload: any;
}