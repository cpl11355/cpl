
const mkEl = () => {
  const el = {
    children: [], dataset: {}, style: new Proxy({}, { get: (o, k) => (k === 'setProperty' ? () => {} : ''), set: () => true }),
    classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
    addEventListener(){}, append(){}, querySelector(){ return mkEl(); },
    querySelectorAll(){ return []; }, getContext(){ return { clearRect(){}, beginPath(){}, moveTo(){}, lineTo(){}, stroke(){}, arc(){}, fill(){} }; },
    getBoundingClientRect(){ return { top: 100, bottom: 900 }; },
    setAttribute(){}, getAttribute(){ return null; },
    scrollIntoView(){}, closest(){ return null; },
    textContent: '', value: '', disabled: false, width: 300, height: 150,
    clientWidth: 300, clientHeight: 150, offsetHeight: 2000,
  };
  return el;
};
const mkList = () => [];
global.document = {
  querySelector: () => mkEl(), querySelectorAll: () => [],
  getElementById: () => mkEl(), createElement: () => mkEl(),
  body: mkEl(), documentElement: mkEl(),
};
global.window = global;
global.addEventListener = () => {};
global.innerHeight = 800; global.scrollY = 0; global.scrollTo = () => {};
global.requestAnimationFrame = () => {};
global.IntersectionObserver = class { constructor(cb){} observe(){} unobserve(){} };
global.performance = { now: () => 0, getEntriesByType: () => [] };
global.history = { scrollRestoration: 'auto', replaceState(){} };
global.location = { hash: '', pathname: '/', search: '' };
global.localStorage = { getItem: () => null, setItem(){} };
const fs = require('fs');
let src = fs.readFileSync('C:/Users/orang/Desktop/网页制作/work/live.js', 'utf8');
try {
  eval(src);
  console.log('LOAD OK — no throw during initial execution');
} catch (e) {
  console.log('LOAD THREW:', e.constructor.name + ':', e.message);
  console.log((e.stack || '').split('\n').slice(0, 4).join('\n'));
}
