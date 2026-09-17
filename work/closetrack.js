var fs = require('fs');
var s = fs.readFileSync('index.html', 'utf8');
var start = s.indexOf('{tagCn:"02');
var q = null, esc = false, ln = s.slice(0, start).split('\n').length;
var cd = 1;
for (var k = start + 1; k < s.length; k++) {
  var c = s[k];
  if (c === '\n') { ln++; continue; }
  if (q) {
    if (esc) { esc = false; }
    else if (c === '\\') { esc = true; }
    else if (c === q) { q = null; }
  } else {
    if (c === '"' || c === "'") { q = c; }
    else if (c === '{') { cd++; console.log('OPEN line ' + ln + ' cd=' + cd); }
    else if (c === '}') { console.log('CLOSE line ' + ln + ' cd=' + cd + ' ctx=' + JSON.stringify(s.slice(k - 40, k))); cd--; if (cd < 0) break; }
  }
  if (ln > 730) break;
}
