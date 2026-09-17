const langButton=document.querySelector('[data-lang-toggle]');
const savedLang=localStorage.getItem('cpl-lang');
if(savedLang)document.body.dataset.lang=savedLang;
if(langButton){const sync=()=>langButton.textContent=document.body.dataset.lang==='en'?'中文':'EN';sync();langButton.addEventListener('click',()=>{document.body.dataset.lang=document.body.dataset.lang==='en'?'zh':'en';localStorage.setItem('cpl-lang',document.body.dataset.lang);sync()})}
const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('on');observer.unobserve(entry.target)}}),{threshold:.14});document.querySelectorAll('.reveal').forEach(element=>observer.observe(element));
