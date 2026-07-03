export class FlagEvent {
    prom;
    promResolve;
    promReject;
    constructor() {
        this.prom = new Promise((res, rej) => {
            this.promResolve = res;
            this.promReject = rej;
        });
    }
    get promise() {
        return this.prom;
    }
    resolve = () => {
        this.promResolve();
    };
    reject = () => {
        this.promReject();
    };
}
var c;
//# sourceMappingURL=FlagEvent.js.map