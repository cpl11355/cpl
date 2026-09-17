var fs = require('fs');
var lines = fs.readFileSync('index.html', 'utf8').split('\n');
for (var i = 783; i <= 787; i++) {
  console.log((i + 1) + ' len=' + lines[i].length + ' tail=' + JSON.stringify(lines[i].slice(-80)));
}
