var fs = require('fs');
var lines = fs.readFileSync('index.html', 'utf8').split('\n');
lines.forEach(function (t, i) {
  if (/route optimization\.|trips the Go|veto\./.test(t)) {
    console.log((i + 1) + ' tail=' + JSON.stringify(t.slice(-30)));
  }
});
