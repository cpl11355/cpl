var fs = require('fs');
var path = require('path');
var p = path.join(process.env.TEMP, 'check3.js');
var s = fs.readFileSync(p, 'utf8');
var i = s.indexOf('const CASES=');
console.log('cases_at=' + i);
var j = s.indexOf('[', i);
var d = 0, q = null, esc = false, k;
for (k = j; k < s.length; k++) {
  var c = s[k];
  if (q) {
    if (esc) { esc = false; }
    else if (c === '\\') { esc = true; }
    else if (c === q) { q = null; }
  } else {
    if (c === '"' || c === "'") { q = c; }
    else if (c === '[') { d++; }
    else if (c === ']') { d--; if (d === 0) { break; } }
  }
}
console.log('end_at=' + k + ' depth=' + d);
var arr = s.slice(j, k + 1);
try {
  var v = eval('(' + arr + ')');
  console.log('EVAL_OK len=' + v.length);
  v.forEach(function (o, n) {
    console.log(n + ' link=' + o.summaryLink + ' secs=' + (o.sumSecs && o.sumSecs.length));
  });
} catch (e) {
  console.log('EVAL_FAIL ' + e.message);
}
