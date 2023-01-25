type messageTypeIncoming = "answer" | "bufferUpdate";
type messageTypeOutgoing = "call";

export interface FrontendlibSocketIncomingMessage {
    message_type: messageTypeIncoming;
    answer_id?: number;
    payload: any;
}

export interface FrontendlibSocketOutgoingMessage {
    message_type: messageTypeOutgoing;
    answer_id: number;
    payload: any;
}