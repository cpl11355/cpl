const fs=require('fs');
const source=fs.readFileSync(process.argv[2]||'index.html','utf8');
const requirements=[
  'class="story-stage"',
  '01 / VALUE',
  '02 / EVIDENCE',
  '03 / SYSTEM',
  'class="story-list"'
];
const missing=requirements.filter(item=>!source.includes(item));
if(missing.length){throw new Error(`Missing immersive story behavior: ${missing.join(', ')}`)}
console.log('Immersive story structure present');
