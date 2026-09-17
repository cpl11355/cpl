var fs = require('fs');
var lines = fs.readFileSync('index.html', 'utf8').split('\n');
var t = lines[721];
console.log('len=' + t.length);
console.log('tail=' + JSON.stringify(t.slice(-60)));
