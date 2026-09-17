var fs = require('fs');
var s = fs.readFileSync('index.html', 'utf8');
var start = s.indexOf('const CASES=');
var line = s.slice(0, start).split('\n').length;
var bd = 0, cd = 0, q = null, esc = false, ln = line;
var cases = 0;
for (var k = start; k < s.length; k++) {
  var c = s[k];
  if (c === '\n') { ln++; continue; }
  if (q) {
    if (esc) { esc = false; }
    else if (c === '\\') { esc = true; }
    else if (c === q) { q = null; }
  } else {
    if (c === '"' || c === "'") { q = c; }
    else if (c === '[') { bd++; }
    else if (c === ']') { bd--; if (bd < 0) { console.log('BRACKET_NEG at line ' + ln); break; } }
    else if (c === '{') { cd++; }
    else if (c === '}') {
      cd--;
      if (cd < 0) { console.log('BRACE_NEG at line ' + ln + ' ctx=' + JSON.stringify(s.slice(k - 60, k + 10))); break; }
      if (cd === 0) { cases++; console.log('CASE_END #' + cases + ' at line ' + ln); if (cases > 6) break; }
    } else if (c === ';' && cd === 0 && bd === 0 && cases >= 5) {
      console.log('ARRAY_STMT_END at line ' + ln);
      break;
    }
  }
  if (k - start > 60000) { console.log('STOP cap, bd=' + bd + ' cd=' + cd + ' ln=' + ln); break; }
}
