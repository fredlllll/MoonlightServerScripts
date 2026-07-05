export interface LogTrackerOptions {
    serverId: string;
    textareaId: string;
    checkboxId: string;
    maxLines?: number;
}

export class LogTracker {
    private readonly serverId: string;
    private readonly wsUrl: string;
    private readonly maxLines: number;

    private textarea: HTMLTextAreaElement | null = null;
    private checkbox: HTMLInputElement | null = null;
    private socket: WebSocket | null = null;
    private isReconnecting = false;
    private reconnectDelay = 1000;
    private logLines: string[] = [];
    private firstConnect: boolean = true;
    private readonly maxReconnectDelay = 16000;

    constructor(options: LogTrackerOptions) {
        this.serverId = options.serverId;
        this.maxLines = options.maxLines ?? 1500;

        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.wsUrl = `${wsProtocol}//${window.location.host}/api/servers/${this.serverId}/ws`;

        this.initElements(options.textareaId, options.checkboxId);
    }

    private initElements(textareaId: string, checkboxId: string): void {
        this.textarea = document.getElementById(textareaId) as HTMLTextAreaElement;
        this.checkbox = document.getElementById(checkboxId) as HTMLInputElement;


        if (!this.textarea || !this.checkbox) {
            console.error(`[LogTracker] Failed to initialize. Check your DOM IDs: #${textareaId}, #${checkboxId}`);
            return;
        }
        this.logLines = this.textarea.value.split('\n') || [];
        this.flush();

        this.setupEventListeners();
    }

    private setupEventListeners(): void {
        if (!this.textarea || !this.checkbox) return;

        // Detect manual upward scroll to disable auto-scroll
        this.textarea.addEventListener('scroll', () => {
            if (!this.checkbox?.checked || !this.textarea) return;

            const scrollBottomOffset = this.textarea.scrollHeight - this.textarea.scrollTop - this.textarea.clientHeight;

            // User scrolled away from bottom (5px buffer)
            if (scrollBottomOffset > 5) {
                this.checkbox.checked = false;
            }
        });

        // Instant snap to bottom if user manually re-enables checking
        this.checkbox.addEventListener('change', () => {
            if (this.checkbox?.checked && this.textarea) {
                this.textarea.scrollTop = this.textarea.scrollHeight;
            }
        });
    }

    public connect(): void {
        if (!this.textarea || !this.checkbox) return;

        console.log(`[LogTracker] Connecting: ${this.wsUrl}`);
        this.socket = new WebSocket(this.wsUrl);

        this.socket.onopen = () => {
            console.log("[LogTracker] Connected successfully.");
            this.isReconnecting = false;
            this.reconnectDelay = 1000;
            if (this.firstConnect) {
                this.firstConnect = false;
            } else {
                this.appendSystemMessage("Connected to live log stream");
            }
        };

        this.socket.onmessage = (event: MessageEvent) => {
            this.appendText(event.data);
        };

        this.socket.onclose = (event: CloseEvent) => {
            console.warn(`[LogTracker] Connection lost (Code: ${event.code}). Attempting reconnect...`);
            this.appendSystemMessage("Connection lost. Reconnecting...");
            this.handleReconnect();
        };

        this.socket.onerror = (error: Event) => {
            console.error("[LogTracker] WebSocket error:", error);
        };
    }

    private handleReconnect(): void {
        if (this.isReconnecting) return;
        this.isReconnecting = true;

        setTimeout(() => {
            this.isReconnecting = false;
            this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay);
            this.connect();
        }, this.reconnectDelay);
    }

    private appendSystemMessage(msg: string): void {
        this.appendText(`[System: ${msg}]`);
    }

    private appendText(text: string): void {
        if (!this.textarea) return;

        // Handle incoming text blocks that might contain internal newlines 
        // (like our system messages or stacked log packets)
        const newLines = text.split('\n');

        for (const line of newLines) {
            this.logLines.push(line);
        }

        // High-performance array shifting instead of repeated heavy string splitting
        if (this.logLines.length > this.maxLines) {
            const linesToRemove = this.logLines.length - this.maxLines;
            this.logLines.splice(0, linesToRemove);
        }

        // One single source of truth flush to the DOM
        this.flush();
    }

    private flush(): void {
        if (!this.textarea) return;
        this.textarea.value = this.logLines.join('\n');

        // Handle scrolling
        if (this.checkbox?.checked) {
            this.textarea.scrollTop = this.textarea.scrollHeight;
        }
    }

    /**
     * Clean teardown if navigating away without destroying the page instance
     */
    public disconnect(): void {
        if (this.socket) {
            this.socket.onclose = null; // Prevent triggers during intentional closing
            this.socket.close();
        }
    }
}