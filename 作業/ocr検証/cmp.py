import json,subprocess,os,datetime
gt=json.load(open('/tmp/body.json'))['days']
out=json.load(open('/tmp/pwt/ocr_out.json'))
src=os.path.expanduser('~/ライフログ/取り込み元/ジム計測値/')
ok=bad=miss=0;rep=[]
for n,r in sorted(out.items()):
  h=n.replace('.jpg','.HEIC')
  d=subprocess.run(['mdls','-raw','-name','kMDItemContentCreationDate',src+h],capture_output=True,text=True).stdout.strip()
  dt=(datetime.datetime.strptime(d[:19],'%Y-%m-%d %H:%M:%S')+datetime.timedelta(hours=9)).strftime('%Y-%m-%d')
  g=gt[dt];line=[n,dt,r.get('page'),str(r.get('ms'))]
  exp={'p1':['w','bmi','bf','vf','mm','bone','bmr','age','ath','mq'],'p2':['fat','ffm','tbw','tbwp','prot','smi'],'pa':['pa'],'parts':['leg']}.get(r.get('page'),[])
  for k in exp:
    gv=g['m'].get(k)
    if gv is None: continue
    if r.get(k) is None: miss+=1;line.append(k+':MISS')
    elif abs(r[k]-gv)<1e-6: ok+=1
    else: bad+=1;line.append(f'{k}:{r[k]}!={gv}')
  if r.get('page')=='parts':
    for k,v in g['parts'].items():
      rv=(r.get('parts') or {}).get(k)
      if rv is None: miss+=1;line.append('parts.'+k+':MISS')
      elif abs(rv-v)<1e-6: ok+=1
      else: bad+=1;line.append(f'parts.{k}:{rv}!={v}')
  if r.get('date'): line.append('date='+r['date']+(' OK' if r['date']==dt else ' NG'))
  if 'err' in r: line.append(r['err'])
  rep.append(' '.join(line))
print('\n'.join(rep));print('ok',ok,'bad',bad,'miss',miss)
