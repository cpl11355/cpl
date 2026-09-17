const fs=require('fs');
const home=fs.readFileSync('index.html','utf8');
const requirements=['id="about"','id="services"','id="cases"','id="future"','id="team"','id="contact"','研究能力实证','capability-story'];
const missing=requirements.filter(item=>!home.includes(item));
if(missing.length)throw new Error(`Homepage details missing: ${missing.join(', ')}`);
console.log('Full homepage detail and immersive capability story present');
