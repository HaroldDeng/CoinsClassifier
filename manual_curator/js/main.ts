type CoinType = 'P' | 'N' | 'D' | 'Q' | 'C' | 'X';
type CoinFace = 'H' | 'T' | 'X';

class Curator {
	private static CLASS_LUT: Map<CoinType | CoinFace, string> = new Map([
		['P', 'penny'],
		['N', 'nickel'],
		['D', 'dime'],
		['Q', 'quarter'],
		['C', 'dollar'],
		['X', 'none'],
		['H', 'heads'],
		['T', 'tails'],
	]);
	private readonly user: string;
	private imgId: string | undefined = undefined;
	readonly img = document.getElementById('main') as HTMLImageElement;
	readonly table = document.getElementById('keys') as HTMLTableElement;
	// State
	private _type: CoinType | undefined;
	private _face: CoinFace | undefined;

	constructor() {
		if (localStorage.getItem('user') === null) {
			this.user = prompt('Enter user name')!;
			localStorage.setItem('user', this.user);
		} else {
			this.user = localStorage.getItem('user')!;
		}
		const body = document.querySelector<HTMLBodyElement>('body')!;
		body.addEventListener('keypress', this.onKeyPress);
	}
	private get classes(): Set<string> {
		const result = new Set<string>();
		if (this._type !== undefined)
			result.add(Curator.CLASS_LUT.get(this._type)!);
		if (this._face !== undefined)
			result.add(Curator.CLASS_LUT.get(this._face)!);
		return result;
	}
	private updateClasses() {
		const wl = this.classes;
		const classes = this.table.classList;
		for (const c of wl)
			classes.add(c);

		for (const c of Curator.CLASS_LUT.values())
			if (!wl.has(c))
				classes.remove(c)
	}
	get type() { return this._type; }
	set type(value: CoinType | undefined) {
		this._type = value;
		this.updateClasses();
	}
	get face() { return this._face; }
	set face(value: CoinFace | undefined) {
		this._face = value;
		this.updateClasses();
	}
	reset() {
		this._type = undefined;
		this._face = undefined;
		this.updateClasses();
	}
	query(path: string, method: string = 'GET', data?: object): Promise<XMLHttpRequest> {
		// Create the XHR request
		var request = new XMLHttpRequest();

		// Return it as a Promise
		return new Promise((resolve, reject) => {
			// Setup our listener to process compeleted requests
			request.addEventListener('readystatechange', () => {
				// Only run if the request is complete
				if (request.readyState !== 4)
					return;
				
				// Process the response
				if (request.status >= 200 && request.status < 300) {
					// If successful
					resolve(request);
				} else {
					// If failed
					reject({
						status: request.status,
						statusText: request.statusText
					});
				}
			});

			// Setup our HTTP request
			request.open(method, path, true);

			// Send the request
			if (method == 'POST' && data !== undefined) {
				request.setRequestHeader('Content-type', 'application/json;charset=UTF-8');
				request.send(JSON.stringify(data));
			} else {
				request.send();
			}
		});
	}
	async advance() {
		console.log('Getting next image');
		const img = await this.query('/api/nextimg');
		console.log(`Get image ${img.responseText}`, img);
		this.imgId = img.responseText;
		this.img.src = `/img/${img.responseText}`;
	}

	async submit() {
		const type = this.type;
		let face = this.face;
		if (type == 'X' && face === undefined)
			face = 'X';
		if (type === undefined || face === undefined)
			return;
		this.reset();
		await this.query('/api/label', 'POST', { name: this.imgId!, type, face, user: this.user});
		await this.advance();
	}

	onKeyPress = (e: KeyboardEvent) => {
		switch (e.code) {
			case 'KeyP':
				this.type = 'P';
				break;
			case 'KeyN':
				this.type = 'N';
				break;
			case 'KeyD':
				this.type = 'D';
				break;
			case 'KeyQ':
				this.type = 'Q';
				break;
			case 'KeyC':
				this.type = 'C';
				break;
			case 'KeyX':
				this.type = 'X';
				break;
			case 'KeyH':
				this.face = 'H';
				break;
			case 'KeyT':
				this.face = 'T';
				break;
			case 'Escape':
			case 'Delete':
				this.reset();
				break;
			case 'Enter':
				this.submit();
				break;
			default:
				return;
		}
		e.preventDefault();
	}
}

const curator = new Curator();
curator.advance();