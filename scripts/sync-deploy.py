#!/usr/bin/env python3
"""Check/vendor the common deployment engine. App profiles and wrappers remain app-owned."""
import argparse,pathlib,shutil,sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
APPS=['pwa','a4','balance','doctools','elementar','eternytimer','festival','flip','freezer','fuel','govio','oficina','sopa_de_letras']
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('apps',nargs='*');args=p.parse_args();bad=[]
source=ROOT/'pwa/shared/deploy/deploy-core.sh'
for app in args.apps or APPS:
 if app not in APPS:p.error('Unknown app: '+app)
 target=ROOT/app/'scripts/deploy-core.sh'
 if target.is_symlink():p.error('Refusing symlink: '+str(target))
 if args.write:shutil.copyfile(source,target)
 if not target.is_file() or target.read_bytes()!=source.read_bytes():bad.append(app)
if bad:print('Deployment engine drift: '+', '.join(bad));sys.exit(1)
print('Shared deploy 1.0.0: all selected local copies match')
