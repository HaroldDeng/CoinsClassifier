/**
 * Format:
 * struct CTSPacket {
 *  id: int32
 *  width: int16
 *  height: int16
 *  data: []
 * }
 */
declare class CTSPacket {
    static wrap(buf: ArrayBufferLike): void;
    static allocate(size: number): void;
    private constructor();
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
declare class STCPacket {
    readonly buffer: ArrayBuffer;
    readonly labels: ReadonlyArray<string>;
    static readonly OFFSET_ID = 0;
    static readonly OFFSET_NUMBOXES: number;
    static readonly OFFSET_BOX0: number;
    protected view: DataView;
    constructor(buffer: ArrayBuffer, labels?: ReadonlyArray<string>);
    [Symbol.iterator](): IterableIterator<CoinAnnotation>;
    id: number;
    numBoxes: number;
    box(i: number): CoinAnnotation;
}
declare class CoinAnnotationView implements CoinAnnotation {
    readonly buffer: ArrayBuffer;
    protected readonly labels: ReadonlyArray<string>;
    protected view: Uint16Array;
    constructor(buffer: ArrayBuffer, labels?: ReadonlyArray<string>);
    labelId: number;
    label: string;
    accuracy: number;
    top: number;
    left: number;
    width: number;
    height: number;
}
declare class STCPacketBuilder {
    private readonly labels;
    id: number;
    private annotations;
    constructor(labels: string[], id?: number);
    append(top: number, left: number, width: number, height: number, label: string | number, accuracy?: number): void;
    build(buffer?: ArrayBuffer): STCPacket;
}
//# sourceMappingURL=packet.d.ts.map