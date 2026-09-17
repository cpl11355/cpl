var fs = require('fs');
var s = fs.readFileSync('index.html', 'utf8');
var i = s.indexOf('const CASES=');
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
var v = eval('(' + s.slice(j, k + 1) + ')');
console.log('CASES len=' + v.length);
v.forEach(function (o, n) {
  var ok = o.summaryLink && o.methodCn && o.methodEn && o.sumSecs && o.sumSecs.length === 5;
  var fileOk = o.summaryLink ? fs.existsSync(o.summaryLink) : false;
  console.log(n + ' ' + (ok ? 'DATA_OK' : 'DATA_BAD') + ' file=' + (fileOk ? 'EXISTS' : 'MISSING') + ' ' + o.summaryLink);
});
var leak = ['HAO YUN', 'Reachin', 'MEI ZHI', 'Yonghui', 'Victor Zhang', '1185 6th'];
leak.forEach(function (w) {
  console.log('leak[' + w + ']=' + (s.indexOf(w) >= 0 ? 'FOUND' : 'clean'));
});
