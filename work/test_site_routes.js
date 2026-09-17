const fs=require('fs');
const pages=['index.html','capabilities.html','research.html','future.html','board.html','contact.html'];
const requiredLinks=['capabilities.html','research.html','future.html','board.html','contact.html'];
const missing=pages.filter(page=>!fs.existsSync(page));
if(missing.length)throw new Error(`Missing story pages: ${missing.join(', ')}`);
const home=fs.readFileSync('index.html','utf8');
const absent=requiredLinks.filter(link=>!home.includes(`href="${link}"`));
if(absent.length)throw new Error(`Homepage navigation missing: ${absent.join(', ')}`);
console.log('Story pages and homepage navigation present');
