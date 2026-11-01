#!/usr/bin/env python3
"""Check/vendor upstream controls. App-owned styles/renderers are never overwritten."""
import argparse, pathlib, shutil, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
SOURCE=ROOT/'pwa/shared/controls'
APPS={'a4':'.','agenda':'public/assets','balance':'.','doctools':'web','elementar':'.','eternytimer':'.','festival':'.','flip':'.','freezer':'.','fuel':'.','govio':'.','oficina':'.','sopa_de_letras':'pwa'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');p.add_argument('apps',nargs='*',choices=None);args=p.parse_args();bad=[]
 for app in args.apps or APPS:
  if app not in APPS:p.error('Unknown app: '+app)
  dest=ROOT/app/APPS[app]
  for name,out in [('controls.css','shared-controls.css'),('icons.svg','shared-icons.svg'),('chevron.svg','shared-chevron.svg')]:
   target=dest/out
   if target.is_symlink():p.error('Refusing symlink: '+str(target))
   if args.write:shutil.copyfile(SOURCE/name,target)
   if not target.is_file() or target.read_bytes()!=(SOURCE/name).read_bytes():bad.append(str(target))
 if bad:print('Control kit drift:\n'+'\n'.join(bad));return 1
 print('Shared controls 1.0.0: all selected local copies match');return 0
if __name__=='__main__':sys.exit(main())
