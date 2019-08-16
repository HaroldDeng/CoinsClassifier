"use strict";
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
    static wrap(buf) {
    }
    static allocate(size) {
    }
    constructor(size) {
    }
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
    constructor(buffer, labels = []) {
        this.buffer = buffer;
        this.labels = labels;
        this.view = new DataView(this.buffer);
    }
    *[Symbol.iterator]() {
        const len = this.numBoxes;
        for (let i = 0; i < len; i++)
            yield this.box(i);
    }
    get id() {
        return this.view.getUint32(STCPacket.OFFSET_ID);
    }
    set id(value) {
        this.view.setUint32(STCPacket.OFFSET_ID, value);
    }
    get numBoxes() {
        return this.view.getUint32(STCPacket.OFFSET_NUMBOXES);
    }
    set numBoxes(v) {
        this.view.setUint32(STCPacket.OFFSET_NUMBOXES, v);
    }
    box(i) {
        if (i > this.numBoxes)
            throw new RangeError(`box ${i} out of bounds`);
        const start = STCPacket.OFFSET_BOX0 + i * 6;
        return new CoinAnnotationView(this.buffer.slice(start, start + 12));
    }
}
STCPacket.OFFSET_ID = 0;
STCPacket.OFFSET_NUMBOXES = STCPacket.OFFSET_ID + 4;
STCPacket.OFFSET_BOX0 = STCPacket.OFFSET_NUMBOXES + 4;
class CoinAnnotationView {
    constructor(buffer, labels = []) {
        this.buffer = buffer;
        this.labels = labels;
        this.view = new Uint16Array(this.buffer);
    }
    get labelId() {
        return this.view[0];
    }
    set labelId(value) {
        this.view[0] = value;
    }
    get label() {
        const id = this.labelId;
        if (id >= this.labels.length)
            return `label${id}`;
        return this.labels[id];
    }
    set label(name) {
        this.labelId = this.labels.indexOf(name);
    }
    get accuracy() {
        return this.view[1] / 65536;
    }
    set accuracy(value) {
        this.view[1] = value * 65536;
    }
    get top() {
        return this.view[2];
    }
    set top(v) {
        this.view[2] = v;
    }
    get left() {
        return this.view[3];
    }
    set left(v) {
        this.view[3] = v;
    }
    get width() {
        return this.view[4];
    }
    set width(v) {
        this.view[4] = v;
    }
    get height() {
        return this.view[5];
    }
    set height(v) {
        this.view[5] = v;
    }
}
class STCPacketBuilder {
    constructor(labels, id = 0) {
        this.labels = labels;
        this.id = id;
        this.annotations = [];
    }
    append(top, left, width, height, label, accuracy = 1) {
        const labelId = (typeof label === 'number') ? label : this.labels.indexOf(label);
        this.annotations.push({ top, left, width, height, label: '', labelId, accuracy });
    }
    build(buffer) {
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
//# sourceMappingURL=packet.js.map