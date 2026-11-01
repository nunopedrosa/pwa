#!/usr/bin/env python3
"""Generate a static directory from apps.txt and app-owned public metadata. No network/dependencies."""
import argparse,hashlib,html,json,pathlib,re,sys,urllib.parse
SITE=pathlib.Path(__file__).resolve().parents[1]
class DirectoryError(ValueError):pass
def text_file(path,limit=262144):
 if not path.is_file():return ''
 if path.stat().st_size>limit:raise DirectoryError('Metadata is too large: '+str(path))
 return path.read_text(encoding='utf-8')
def folders(config):
 values=[]
 for line in config.splitlines():
  name=line.split('#',1)[0].strip()
  if not name:continue
  if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*',name):raise DirectoryError('Use a simple sibling folder name: '+name)
  if name in values:raise DirectoryError('Duplicate folder: '+name)
  values.append(name)
 return values

def public_url(value):
 try:
  p=urllib.parse.urlsplit(value)
  port=p.port
 except ValueError as error:raise DirectoryError('Invalid public HTTPS URL: '+value) from error
 if p.scheme!='https' or not p.hostname or p.username or p.password or p.query or p.fragment:raise DirectoryError('Invalid public HTTPS URL: '+value)
 if port is not None and not 1<=port<=65535:raise DirectoryError('Invalid public HTTPS port: '+value)
 return urllib.parse.urlunsplit(('https',p.netloc,p.path.rstrip('/')+'/', '', ''))

def metadata(root,name):
 folder=root/name
 if not folder.is_dir() or folder.is_symlink():raise DirectoryError('Missing or symlinked app folder: '+name)
 profile=text_file(folder/'scripts/deploy-profile.sh')
 source=re.search(r'^SOURCE_SUBDIR=([A-Za-z0-9_./-]+)\s*$',profile,re.M)
 runtime=(folder/source[1] if source else folder).resolve()
 if not runtime.is_relative_to(folder.resolve()):raise DirectoryError('Public source escapes app folder: '+name)
 candidates=[runtime]+[folder/d for d in ['public','web','pwa'] if folder/d!=runtime]
 manifest={};manifest_path=None
 for candidate in candidates:
  for filename in ['manifest.webmanifest','manifest.json']:
   p=candidate/filename
   if p.is_file():
    if not p.resolve().is_relative_to(folder.resolve()):raise DirectoryError('Manifest escapes app folder: '+name)
    try:manifest=json.loads(text_file(p))
    except (ValueError,UnicodeError) as error:raise DirectoryError('Invalid manifest for '+name) from error
    manifest_path=p;break
  if manifest_path:break
 if not isinstance(manifest,dict) or not isinstance(manifest.get('name'),str) or not manifest['name'].strip():raise DirectoryError('Missing manifest name for '+name)
 display=manifest['name'].strip()
 if len(display)>48 and isinstance(manifest.get('short_name'),str) and manifest['short_name'].strip():display=manifest['short_name'].strip()
 if len(display)>120:raise DirectoryError('App name too long: '+name)
 deploy=re.search(r'^DEPLOY_URL=(.*)$',profile,re.M)
 url=re.search(r'https://[^\s\"\'{}<>$]+',deploy[1]) if deploy else None
 if url:url=url[0]
 else:
  # An app without a deploy profile may publish its absolute manifest ID, or
  # document its own site. Ignore repository/provider/documentation URLs.
  identifier=manifest.get('id','')
  if isinstance(identifier,str) and identifier.startswith('https://'):url=identifier
  else:
   excluded={'github.com','www.github.com','developer.mozilla.org','localhost'}
   for document in ['AGENTS.md','README.md']:
    for candidate in re.findall(r'https://[A-Za-z0-9.-]+(?::[0-9]+)?(?:/[A-Za-z0-9._~!$&*+,;=:@%/-]*)?',text_file(folder/document)):
     host=urllib.parse.urlsplit(candidate).hostname
     if host and host not in excluded and (host.endswith('.basecentral.link') or host.endswith('.trekm.com')):url=candidate;break
    if url:break
 if not url:raise DirectoryError('No public URL found for '+name+'; document its deployment URL in the app')
 url=public_url(url)
 icons=manifest.get('icons',[]);icon=''
 if isinstance(icons,list):
  candidates=[i for i in icons if isinstance(i,dict) and isinstance(i.get('src'),str)]
  candidates.sort(key=lambda i:(i.get('type')!='image/svg+xml','192' not in str(i.get('sizes',''))))
  for item in candidates:
   candidate=urllib.parse.urljoin(url,item['src'])
   p=urllib.parse.urlsplit(candidate)
   if p.scheme=='https' and p.netloc==urllib.parse.urlsplit(url).netloc and not p.username and not p.password:
    icon=candidate;break
 return {'folder':name,'name':display,'url':url,'hostname':urllib.parse.urlsplit(url).netloc,'icon':icon}

def render(apps,digest):
 links=[];escape=html.escape
 for app in apps:
  initial=escape(app['name'][0].upper())
  image='<img src="'+escape(app['icon'],quote=True)+'" alt="" width="48" height="48" loading="lazy" decoding="async" referrerpolicy="no-referrer">' if app['icon'] else ''
  links.append('          <li><a class="app-link" href="'+escape(app['url'],quote=True)+'"><span class="app-artwork" aria-hidden="true"><span class="app-initial">'+initial+'</span>'+image+'</span><span class="app-copy"><span class="app-name">'+escape(app['name'])+'</span><span class="hostname">'+escape(app['hostname'])+'</span></span><svg class="open-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 17 17 7M7 7h10v10"/></svg></a></li>')
 template=(SITE/'templates/directory.html').read_text()
 if not links:links=['          <li class="empty">No apps are listed at the moment.</li>']
 style_version=hashlib.sha256((SITE/'styles.css').read_bytes()).hexdigest()[:12]
 return template.replace('{{CONFIG_HASH}}',digest).replace('{{STYLE_VERSION}}',style_version).replace('{{APP_LINKS}}','\n'.join(links))

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=pathlib.Path,default=SITE.parent);parser.add_argument('--site',type=pathlib.Path,default=SITE);parser.add_argument('--check',action='store_true');args=parser.parse_args()
 try:
  config=text_file(args.site/'apps.txt');apps=[metadata(args.root.resolve(),name) for name in folders(config)]
  digest=hashlib.sha256((args.site/'apps.txt').read_bytes()).hexdigest();output=render(apps,digest)
  registry='# Application registry\n\nGenerated from `apps.txt` and each app’s own manifest/deployment documentation. Edit only the folder list to change the selection or order; run `python3 scripts/build-directory.py` locally before committing. URLs are configured destinations, not a live-availability guarantee.\n\n| App | Folder | Site |\n| --- | --- | --- |\n'+''.join('| '+a['name'].replace('|','\\|')+' | `../'+a['folder']+'` | ['+a['hostname']+']('+a['url']+') |\n' for a in apps)+'\nApp-specific storage, compatibility, accounts and backup contracts remain in each app’s own instructions and README. The directory reads no app storage and introduces no shared account or data service.\n'
  outputs={args.site/'index.html':output,args.site/'docs/APPS.md':registry}
  if args.check:
   stale=[str(p) for p,s in outputs.items() if not p.is_file() or p.read_text()!=s]
   if stale:raise DirectoryError('Generated directory is stale: '+', '.join(stale))
  else:
   # Validate all metadata before writing any output; malformed selections preserve the old site.
   for p,s in outputs.items():p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
  print(('Checked' if args.check else 'Generated')+' directory: '+str(len(apps))+' apps')
  return 0
 except (DirectoryError,OSError) as error:print('Directory build stopped: '+str(error),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
