
/**
 * Format:
 * struct CTSPacket {
 *  id: int32
 *  width: int16
 *  height: int16
 *  data: []
 * }
 */
class CTSPacket {
    static wrap(buf: ArrayBufferLike) {

    }
    static allocate(size: number) {

    }
    private constructor(size: number) {

    }
}

interface CoinAnnotation {
    label: string;
    labelId: number;
    accuracy: number;
    top: number;
    left: number;
    width: number;
    height: number;
}

/**
 * Format:
 * struct STCPacket {
 *  id: int32
 *  numBoxes: int32
 *  boxes: {
 *      labelId: int16
 *      p: int16
 *      x: int16
 *      y: int16
 *      w: int16
 *      h: int16
 *  } [numBoxes]
 * }
 */
class STCPacket {
    static readonly OFFSET_ID = 0;
    static readonly OFFSET_NUMBOXES = STCPacket.OFFSET_ID + 4;
    static readonly OFFSET_BOX0 = STCPacket.OFFSET_NUMBOXES + 4;
    
    protected view: DataView = new DataView(this.buffer);
    constructor(readonly buffer: ArrayBuffer, readonly labels: ReadonlyArray<string> = []) {
    }

    *[Symbol.iterator]() {
        const len = this.numBoxes;
        for (let i = 0; i < len; i++)
            yield this.box(i);
    }

    get id(): number {
        return this.view.getUint32(STCPacket.OFFSET_ID);
    }
    set id(value: number) {
        this.view.setUint32(STCPacket.OFFSET_ID, value);
    }
    get numBoxes(): number {
        return this.view.getUint32(STCPacket.OFFSET_NUMBOXES);
    }
    set numBoxes(v: number) {
        this.view.setUint32(STCPacket.OFFSET_NUMBOXES, v);
    }
    box(i: number): CoinAnnotation {
        if (i > this.numBoxes)
            throw new RangeError(`box ${i} out of bounds`);
        const start = STCPacket.OFFSET_BOX0 + i * 6;
        return new CoinAnnotationView(this.buffer.slice(start, start + 12));
    }
}

class CoinAnnotationView implements CoinAnnotation {
    protected view = new Uint16Array(this.buffer);
    constructor(readonly buffer: ArrayBuffer, protected readonly labels: ReadonlyArray<string> = []) {
    }
    get labelId(): number {
        return this.view[0];
    }
    set labelId(value: number) {
        this.view[0] = value;
    }
    get label(): string {
        const id = this.labelId;
        if (id >= this.labels.length)
            return `label${id}`;
        return this.labels[id];
    }
    set label(name: string) {
        this.labelId = this.labels.indexOf(name);
    }
    get accuracy(): number {
        return this.view[1] / 65536;
    }
    set accuracy(value: number) {
        this.view[1] = value * 65536;
    }
    get top(): number {
        return this.view[2];
    }
    set top(v: number) {
        this.view[2] = v;
    }
    get left(): number {
        return this.view[3];
    }
    set left(v: number) {
        this.view[3] = v;
    }
    get width(): number {
        return this.view[4];
    }
    set width(v: number) {
        this.view[4] = v;
    }
    get height(): number {
        return this.view[5];
    }
    set height(v: number) {
        this.view[5] = v;
    }
}

class STCPacketBuilder {
    private annotations: CoinAnnotation[] = [];

    constructor(private readonly labels: string[], public id: number = 0) {
    }

    append(top: number, left: number, width: number, height: number, label: string | number, accuracy: number = 1) {
        const labelId = (typeof label === 'number') ? label : this.labels.indexOf(label);
        this.annotations.push({top, left, width, height, label: '', labelId, accuracy });
    }

    build(buffer?: ArrayBuffer): STCPacket {
        const buffLen = STCPacket.OFFSET_BOX0 + 6 * this.annotations.length;
        if (buffer == undefined)
            buffer = new ArrayBuffer(buffLen);
        const arr = new Uint16Array(buffer, STCPacket.OFFSET_BOX0);
        for (let i = 0; i < this.annotations.length; i++) {
            const c = this.annotations[i];
            arr[i * 6 + 0] = c.labelId;
            arr[i * 6 + 1] = c.accuracy * 65535;
            arr[i * 6 + 2] = c.top;
            arr[i * 6 + 3] = c.left;
            arr[i * 6 + 4] = c.width;
            arr[i * 6 + 5] = c.height;
        }
        const result = new STCPacket(buffer, this.labels);
        result.id = this.id;
        result.numBoxes = this.annotations.length;
        return result;
    }
}