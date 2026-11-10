p="kintore-app/index.html";s=open(p,encoding="utf-8").read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:50];s=s.replace(a,b)
rep("  for(var k=5;k>=1;k--){if(end-k>=0) tone(end-k,0.15,880);}",
    "  for(var k=5;k>=1;k--){if(end-k>=0){tone(end-k,0.08,880);tone(end-k+0.14,0.08,880);}}")
rep("""    var t=actx.currentTime,o=actx.createOscillator(),g=actx.createGain(),d=long?0.8:0.15;
    o.type="sine";o.frequency.value=long?1320:880;
    g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(0.6,t+0.01);
    g.gain.setValueAtTime(0.6,t+d-0.05);g.gain.exponentialRampToValueAtTime(0.0001,t+d);
    o.connect(g);g.connect(actx.destination);o.start(t);o.stop(t+d+0.02);""",
"""    var t0=actx.currentTime;
    function one(t,d,f){var o=actx.createOscillator(),g=actx.createGain();o.type="sine";o.frequency.value=f;
      g.gain.setValueAtTime(0.0001,t);g.gain.exponentialRampToValueAtTime(0.6,t+0.01);
      g.gain.setValueAtTime(0.6,t+d-0.02);g.gain.exponentialRampToValueAtTime(0.0001,t+d);
      o.connect(g);g.connect(actx.destination);o.start(t);o.stop(t+d+0.02);}
    if(long) one(t0,0.8,1320); else {one(t0,0.08,880);one(t0+0.14,0.08,880);}""")
rep("/* 残り5秒から毎秒ピッ、","/* 残り5秒から毎秒ピッピ、")
open(p,"w",encoding="utf-8").write(s)
q="kintore-app/sw.js";t=open(q,encoding="utf-8").read();assert 'VERSION = "v38"' in t
open(q,"w",encoding="utf-8").write(t.replace('VERSION = "v38"','VERSION = "v39"'));print("ok")
