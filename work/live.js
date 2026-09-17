
function applyLang(mode){
  document.body.dataset.lang=mode;
  document.documentElement.lang=mode==='en'?'en':'zh-CN';
  document.querySelectorAll('[data-ph-zh]').forEach(el=>{
    el.placeholder = mode==='en' ? (el.dataset.phEn||'') : mode==='zh' ? (el.dataset.phZh||'') : ((el.dataset.phZh||'')+' · '+(el.dataset.phEn||''));
  });
  const top=document.getElementById('toTop');
  if(top)top.title = mode==='en'?'Back to top':mode==='zh'?'回到顶部':'回到顶部 Back to top';
}
document.querySelectorAll('.lang-sw button').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('.lang-sw button').forEach(x=>x.classList.remove('on'));
  b.classList.add('on');
  applyLang(b.dataset.set);
}));
applyLang(document.body.dataset.lang||'zh');
document.body.classList.add('fadeimg');
document.querySelectorAll('img').forEach(im=>{
  const show=()=>im.classList.add('ld');
  if(im.complete&&im.naturalWidth)show();
  else{im.addEventListener('load',show);im.addEventListener('error',show)}
});
document.getElementById('contactForm').addEventListener('submit',function(e){
  e.preventDefault();
  const mode=document.body.dataset.lang, btn=this.querySelector('button');
  const v=id=>((document.getElementById(id)||{}).value||'').trim();
  const subject=((mode==='en'?'Consultation inquiry from ':'咨询需求 — ')+v('fName'))||(mode==='en'?'Consultation inquiry':'咨询需求');
  const body=[(mode==='en'?'Name: ':'姓名：')+v('fName'),(mode==='en'?'Email: ':'邮箱：')+v('fEmail'),(mode==='en'?'Type: ':'需求类型：')+v('fType'),'',v('fMsg')].join('\n');
  try{location.href='mailto:cplbiopharma@proton.me?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);}catch(_){}
  btn.textContent = mode==='en' ? '✓ Opening your mail app — we will respond shortly' : mode==='zh' ? '✓ 正在调起邮件发送，我们会尽快与您联系' : '✓ 正在调起邮件 Opening mail app — we will respond shortly';
  btn.disabled=true;
});
(function(){
  const mini=document.getElementById('miniMap'), box=document.getElementById('mapLightbox');
  if(!mini||!box)return;
  const frame=box.querySelector('iframe'), close=document.getElementById('mapClose');
  function open(){ if(frame&&!frame.src)frame.src=frame.dataset.src; box.classList.add('open'); box.setAttribute('aria-hidden','false'); document.body.style.overflow='hidden'; }
  function shut(){ box.classList.remove('open'); box.setAttribute('aria-hidden','true'); document.body.style.overflow=''; }
  mini.addEventListener('click',open);
  mini.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();open()}});
  close.addEventListener('click',shut);
  box.addEventListener('click',e=>{if(e.target===box)shut()});
  addEventListener('keydown',e=>{if(e.key==='Escape')shut()});
})();
document.querySelectorAll('#services .card').forEach((el,i)=>el.classList.add(i%2?'rv-right':'rv-left'));
document.querySelectorAll('#about .card, .value, .step, .banner-strip, .f-box, .f-imgs figure').forEach(el=>{if(!el.classList.contains('reveal'))el.classList.add('reveal')});
document.querySelectorAll('section .wrap>.kicker, section .wrap>h2.title, section .wrap>p.lead:first-of-type, .proof-rail, .case-cta, .nf, .member, .contact-box>*').forEach(el=>{if(!el.classList.contains('reveal'))el.classList.add('reveal')});
document.querySelectorAll('.img-frame, .banner-strip, .proof-rail, .case-cta, .member').forEach(el=>el.classList.add('reveal-scale'));
function revealDelay(index){return Math.min(index*90,360)}
['.grid2','.grid3','.process','.nowfuture','.future-grid'].forEach(selector=>document.querySelectorAll(selector).forEach(group=>Array.from(group.children).filter(el=>el.classList.contains('reveal')).forEach((el,index)=>el.style.setProperty('--reveal-delay',`${revealDelay(index)}ms`))));
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
const header=document.querySelector('header'), toTop=document.getElementById('toTop'), heroBg=document.querySelector('.hero-bg'), heroInner=document.querySelector('.hero-inner');
const scenes=[...document.querySelectorAll('.scene')];
function syncScenes(){scenes.forEach(scene=>{const rect=scene.getBoundingClientRect(),progress=Math.max(0,Math.min(1,(innerHeight-rect.top)/(innerHeight+rect.height))),shift=Math.round((progress-.5)*46);scene.style.setProperty('--scene-shift',`${shift}px`);scene.style.setProperty('--scene-shift-soft',`${Math.round(-shift*.45)}px`);scene.classList.toggle('is-live',rect.top<innerHeight*.7&&rect.bottom>innerHeight*.3)})}
const scrollProgress=document.getElementById('scrollProgress');
const journeyStory=document.querySelector('.journey-story'),journeyStages=[...document.querySelectorAll('.journey-stage')];
function syncJourney(){if(!journeyStory)return;const rect=journeyStory.getBoundingClientRect(),travel=Math.max(1,journeyStory.offsetHeight-innerHeight),progress=Math.max(0,Math.min(1,-rect.top/travel)),step=Math.min(journeyStages.length-1,Math.floor(progress*journeyStages.length));journeyStory.style.setProperty('--j-scale',(progress*.3).toFixed(3));journeyStory.style.setProperty('--j-core',(progress*.7).toFixed(3));journeyStages.forEach((stage,index)=>stage.classList.toggle('is-active',index===step));}
const pinStories=[...document.querySelectorAll('.capability-story')],futurePortal=document.querySelector('.future-portal');
function syncPinStories(){pinStories.forEach(story=>{const rect=story.getBoundingClientRect(),travel=Math.max(1,story.offsetHeight-innerHeight),progress=Math.max(0,Math.min(1,-rect.top/travel)),step=Math.min(stages.length-1,Math.floor(progress*stages.length));story.style.setProperty('--story-drift',`${Math.round((progress-.5)*140)}px`);story.style.setProperty('--story-grid',`${Math.round(progress*130)}px`);story.style.setProperty('--story-scale',(progress*.46).toFixed(3));story.style.setProperty('--story-core',(progress*.8).toFixed(3));story.style.setProperty('--story-turn',Math.round(progress*92));stages.forEach((stage,index)=>stage.classList.toggle('is-active',index===step));});const first=pinStories[0];if(first){const r=first.getBoundingClientRect();document.body.classList.toggle('story-dark',r.top<innerHeight*.45&&r.bottom>innerHeight*.55);}if(futurePortal){const portalRect=futurePortal.getBoundingClientRect(),portalProgress=Math.max(0,Math.min(1,(innerHeight-portalRect.top)/(innerHeight+portalRect.height)));futurePortal.style.setProperty('--portal-scale',(1+portalProgress*.14).toFixed(3))}}
addEventListener('scroll',()=>{
  header.classList.toggle('scrolled',scrollY>10);
  toTop.classList.toggle('show',scrollY>600);
  if(scrollProgress){const h=document.documentElement,max=h.scrollHeight-h.clientHeight;scrollProgress.style.width=(max>0?(h.scrollTop/max*100):0)+'%';}
  if(heroInner){if(scrollY<innerHeight){const p=Math.min(1,scrollY/innerHeight);heroInner.style.opacity=1-p*.85;heroInner.style.transform="translateY("+(scrollY*.12)+"px) scale("+(1-p*.04)+")";}else{heroInner.style.opacity="";heroInner.style.transform="";}}
  if(heroBg&&scrollY<700)heroBg.style.transform=`translateY(${scrollY*.25}px)`;
  syncScenes();
  syncPinStories();
  syncJourney();
},{passive:true});
addEventListener('resize',()=>{syncScenes();syncPinStories();syncJourney();},{passive:true});
syncScenes();
syncPinStories();
syncJourney();
toTop.addEventListener('click',()=>scrollTo({top:0,behavior:'smooth'}));
const hamb=document.getElementById('hamb'),mMenu=document.getElementById('mMenu');
hamb.addEventListener('click',()=>{hamb.classList.toggle('open');mMenu.classList.toggle('open')});
mMenu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{hamb.classList.remove('open');mMenu.classList.remove('open')}));
const cover=document.getElementById('cover'),cv=document.getElementById('coverCanvas'),ctx=cv.getContext('2d');
let pts=[],coverGone=false;
function cvSize(){cv.width=cover.clientWidth;cv.height=cover.clientHeight}
cvSize();addEventListener('resize',()=>{if(!coverGone)cvSize()});
for(let i=0;i<90;i++)pts.push({x:Math.random(),y:Math.random(),vx:(Math.random()-.5)*.0009,vy:(Math.random()-.5)*.0009,r:Math.random()*1.6+.6});
function drawCover(){
  if(coverGone)return;
  requestAnimationFrame(drawCover);
  const W=cv.width,H=cv.height;ctx.clearRect(0,0,W,H);
  pts.forEach(p=>{p.x=(p.x+p.vx+1)%1;p.y=(p.y+p.vy+1)%1});
  for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){
    const a=pts[i],b=pts[j],dx=(a.x-b.x)*W,dy=(a.y-b.y)*H,d=Math.hypot(dx,dy);
    if(d<130){ctx.strokeStyle=`rgba(0,194,209,${(1-d/130)*.28})`;ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(a.x*W,a.y*H);ctx.lineTo(b.x*W,b.y*H);ctx.stroke()}
  }
  pts.forEach(p=>{ctx.fillStyle='rgba(140,220,255,.85)';ctx.beginPath();ctx.arc(p.x*W,p.y*H,p.r,0,7);ctx.fill()});
}
drawCover();
function enterSite(){cover.classList.add('leave');document.body.classList.remove('cover-on');setTimeout(()=>{cover.style.display='none';coverGone=true},750)}
document.getElementById('enterBtn').addEventListener('click',enterSite);
document.getElementById('replay').addEventListener('click',e=>{e.preventDefault();cover.style.display='flex';requestAnimationFrame(()=>cover.classList.remove('leave'));document.body.classList.add('cover-on');cvSize();coverGone=false;drawCover()});
document.querySelectorAll('.cap-tabs button').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('.cap-tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');
  document.querySelectorAll('.cap-panel').forEach((p,i)=>p.classList.toggle('on',i==b.dataset.cap));
}));
const secs=['about','services','cases','future','team','contact'].map(id=>document.getElementById(id));
const sio=new IntersectionObserver(es=>es.forEach(e=>{
  if(!e.isIntersecting)return;const id=e.target.id;
  document.querySelectorAll('.links a').forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+id));
}),{rootMargin:'-40% 0px -55% 0px'});
secs.forEach(s=>s&&sio.observe(s));
document.querySelectorAll('.story-stage[id]').forEach((el)=>{
  el.style.scrollMarginTop='84px';
});
document.querySelectorAll('[data-sample-cn]').forEach(a=>{
  a.addEventListener('click',()=>{
    const mode=document.body.dataset.lang;
    const inp=document.querySelector('#contactForm input[data-ph-zh]');
    if(inp)inp.value = mode==='en' ? (a.dataset.sampleEn||'') : (a.dataset.sampleCn||'');
  });
});
function skipCoverFast(){cover.style.display='none';coverGone=true;document.body.classList.remove('cover-on');}
function isReloadNav(){
  try{
    var nav=performance.getEntriesByType&&performance.getEntriesByType('navigation')[0];
    if(nav&&nav.type)return nav.type==='reload';
  }catch(_){}
  try{return performance.navigation&&performance.navigation.type===1;}catch(_){return false;}
}
function handleDeepLink(){
  if(isReloadNav()){
    if(location.hash){try{history.replaceState(null,'',location.pathname+location.search);}catch(_){}}
    return;
  }
  const h=location.hash;
  if(!h||h.length<2)return;
  let el=null;try{el=document.querySelector(h);}catch(_){el=null;}
  if(!el)return;
  skipCoverFast();
  setTimeout(()=>{el.scrollIntoView({behavior:'auto',block:'start'})},60);
}
handleDeepLink();
addEventListener('pageshow',handleDeepLink);
