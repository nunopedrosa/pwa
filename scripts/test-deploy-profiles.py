"""Exercise actual profiles and local engines against temporary Git checkouts/public trees."""
import hashlib,os,pathlib,re,shutil,subprocess,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
APPS=['pwa','a4','balance','doctools','elementar','eternytimer','festival','flip','freezer','fuel','govio','oficina','sopa_de_letras']
def git(*args):return subprocess.run(['git',*args],check=True,capture_output=True,text=True)
class Profiles(unittest.TestCase):
 def exercise(self,app):
  source=ROOT/app;profile=(source/'scripts/deploy-profile.sh').read_text();sub=re.search(r'^SOURCE_SUBDIR=(.*)$',profile,re.M)[1];files=re.search(r"PUBLIC_FILES=\$\(cat <<'PUBLIC_FILES'\n([\s\S]*?)\nPUBLIC_FILES\n\)",profile)[1].splitlines()
  with tempfile.TemporaryDirectory(prefix='profile-'+app+'-') as temp:
   base=pathlib.Path(temp);origin=base/'origin';origin.mkdir();(origin/'scripts').mkdir()
   for name in ['deploy.sh','deploy-core.sh','deploy-profile.sh']:
    shutil.copyfile(source/'scripts'/name,origin/'scripts'/name)
   if app=='pwa':shutil.copyfile(source/'apps.txt',origin/'apps.txt')
   if app=='doctools':shutil.copyfile(source/'scripts/deploy-hashes.txt',origin/'scripts/deploy-hashes.txt')
   missing=[]
   for name in files:
    src=source/sub/name;dest=origin/sub/name
    if not src.is_file():missing.append(name);continue
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
   if app=='festival':
    (origin/'hosting').mkdir();shutil.copyfile(source/'hosting/dreamhost.htaccess',origin/'hosting/dreamhost.htaccess');shutil.copyfile(source/'deploy-files.txt',origin/'deploy-files.txt')
   git('init','-b','main',str(origin));git('-C',str(origin),'config','user.name','Test');git('-C',str(origin),'config','user.email','test@example.invalid');git('-C',str(origin),'add','-A');git('-C',str(origin),'commit','-m','profile fixture')
   repo=base/'repo';git('clone',str(origin),str(repo));site=base/'public';site.mkdir();(site/'keep.txt').write_text('host file')
   env=dict(os.environ,BALANCE_BACKUP_DIR=str(base/'private-backups'))
   if app=='doctools':
    release_root=base/'app/releases';old=release_root/'old';(old/'web').mkdir(parents=True);site=base/'app/current';site.symlink_to(old,target_is_directory=True);env['DOCTOOLS_RELEASE_ROOT']=str(release_root)
   result=subprocess.run(['/bin/bash',str(repo/'scripts/deploy.sh'),'--no-pull',str(site)],capture_output=True,text=True,env=env)
   if missing:
    self.assertEqual(app,'govio');self.assertNotEqual(result.returncode,0,result.stdout);self.assertFalse((site/'index.php').exists());return
   self.assertEqual(result.returncode,0,result.stdout+result.stderr)
   public=site/'web' if app=='doctools' else site
   for name in files:self.assertTrue((public/name).is_file(),app+': missing '+name)
   self.assertFalse((public/'scripts').exists());self.assertFalse((public/'AGENTS.md').exists())
   if app!='doctools':self.assertEqual((public/'keep.txt').read_text(),'host file')
   if app=='oficina':
    build=re.search(r"BAYBOOK_BUILD = '([^']+)'",(source/'js/config.js').read_text())[1];self.assertIn('?v='+build,(public/'js/sync.js').read_text());self.assertIn('?v='+build,(public/'index.html').read_text());self.assertTrue((public/'api/sync.php').is_file());self.assertFalse((public/'scripts/setup-sync.php').exists())
   if app=='balance':self.assertEqual(len(list((base/'private-backups').glob('*.tar.gz'))),1)
   if app=='doctools':self.assertEqual(site.resolve().stat().st_mode&0o777,0o755)
for app in APPS:
 setattr(Profiles,'test_'+app,lambda self,app=app:self.exercise(app))
if __name__=='__main__':unittest.main()
