export class FlagEvent {
    private prom: Promise<void>;
    private promResolve: any;
    private promReject: any;
    public constructor() {
        this.prom = new Promise((res, rej) => {
            this.promResolve = res;
            this.promReject = rej;
        });
    }

    public get promise() {
        return this.prom;
    }

    public resolve = () => {
        this.promResolve();
    }

    public reject = () => { //TODO: maybe add something to pass an error?
        this.promReject();
    }
}

var c: PromiseLike<any>;