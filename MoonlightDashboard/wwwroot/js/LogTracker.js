export class LogTracker {
    serverId;
    wsUrl;
    maxLines;
    textarea = null;
    checkbox = null;
    socket = null;
    isReconnecting = false;
    reconnectDelay = 1000;
    logLines = [];
    firstConnect = true;
    maxReconnectDelay = 16000;
    constructor(options) {
        this.serverId = options.serverId;
        this.maxLines = options.maxLines ?? 1500;
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        this.wsUrl = `${wsProtocol}//${window.location.host}/api/servers/${this.serverId}/ws`;
        this.initElements(options.textareaId, options.checkboxId);
    }
    initElements(textareaId, checkboxId) {
        this.textarea = document.getElementById(textareaId);
        this.checkbox = document.getElementById(checkboxId);
        if (!this.textarea || !this.checkbox) {
            console.error(`[LogTracker] Failed to initialize. Check your DOM IDs: #${textareaId}, #${checkboxId}`);
            return;
        }
        this.logLines = this.textarea.value.split('\n') || [];
        this.flush();
        this.setupEventListeners();
    }
    setupEventListeners() {
        if (!this.textarea || !this.checkbox)
            return;
        // Detect manual upward scroll to disable auto-scroll
        this.textarea.addEventListener('scroll', () => {
            if (!this.checkbox?.checked || !this.textarea)
                return;
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
    connect() {
        if (!this.textarea || !this.checkbox)
            return;
        console.log(`[LogTracker] Connecting: ${this.wsUrl}`);
        this.socket = new WebSocket(this.wsUrl);
        this.socket.onopen = () => {
            console.log("[LogTracker] Connected successfully.");
            this.isReconnecting = false;
            this.reconnectDelay = 1000;
            if (this.firstConnect) {
                this.firstConnect = false;
            }
            else {
                this.appendSystemMessage("Connected to live log stream");
            }
        };
        this.socket.onmessage = (event) => {
            this.appendText(event.data);
        };
        this.socket.onclose = (event) => {
            console.warn(`[LogTracker] Connection lost (Code: ${event.code}). Attempting reconnect...`);
            this.appendSystemMessage("Connection lost. Reconnecting...");
            this.handleReconnect();
        };
        this.socket.onerror = (error) => {
            console.error("[LogTracker] WebSocket error:", error);
        };
    }
    handleReconnect() {
        if (this.isReconnecting)
            return;
        this.isReconnecting = true;
        setTimeout(() => {
            this.isReconnecting = false;
            this.reconnectDelay = Math.min(this.reconnectDelay * 2, this.maxReconnectDelay);
            this.connect();
        }, this.reconnectDelay);
    }
    appendSystemMessage(msg) {
        this.appendText(`[System: ${msg}]`);
    }
    appendText(text) {
        if (!this.textarea)
            return;
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
    flush() {
        if (!this.textarea)
            return;
        this.textarea.value = this.logLines.join('\n');
        // Handle scrolling
        if (this.checkbox?.checked) {
            this.textarea.scrollTop = this.textarea.scrollHeight;
        }
    }
    /**
     * Clean teardown if navigating away without destroying the page instance
     */
    disconnect() {
        if (this.socket) {
            this.socket.onclose = null; // Prevent triggers during intentional closing
            this.socket.close();
        }
    }
}
//# sourceMappingURL=LogTracker.js.map