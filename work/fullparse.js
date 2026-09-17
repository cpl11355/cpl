var fs = require('fs');
var vm = require('vm');
var s = fs.readFileSync('index.html', 'utf8');
var m = s.match(/<script>([\s\S]*?)<\/script>/g);
console.log('blocks=' + m.length);
var last = m[m.length - 1].replace(/^<script>/, '').replace(/<\/script>$/, '');
try {
  new vm.Script(last, { filename: 'inline.js' });
  console.log('PARSE_OK len=' + last.length);
} catch (e) {
  console.log('PARSE_FAIL: ' + e.message);
  console.log((e.stack || '').split('\n').slice(0, 6).join('\n'));
}
