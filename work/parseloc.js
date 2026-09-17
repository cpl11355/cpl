var fs = require('fs');
var path = require('path');
var vm = require('vm');
var p = path.join(process.env.TEMP, 'check3.js');
var s = fs.readFileSync(p, 'utf8');
try {
  new vm.Script(s, { filename: 'check3.js' });
  console.log('PARSE_OK');
} catch (e) {
  console.log('PARSE_FAIL: ' + e.message);
  console.log((e.stack || '').split('\n').slice(0, 8).join('\n'));
}
