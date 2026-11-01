"""Behavioral deploy tests: disposable Git upstreams and web roots, never production."""
import pathlib,shutil,subprocess,tempfile,unittest,os
CORE=pathlib.Path(__file__).resolve().parents[1]/'shared/deploy/deploy-core.sh'
class DeployTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='shared-deploy-');self.addCleanup(self.tmp.cleanup);self.root=pathlib.Path(self.tmp.name);self.origin=self.root/'origin';self.repo=self.root/'checkout';self.site=self.root/'public';self.site.mkdir();self.origin.mkdir()
  self.git('init','-b','main',str(self.origin));self.git('-C',str(self.origin),'config','user.email','test@example.invalid');self.git('-C',str(self.origin),'config','user.name','Test')
  (self.origin/'scripts').mkdir();(self.origin/'scripts/deploy-core.sh').write_bytes(CORE.read_bytes() if CORE.exists() else b'#!/bin/bash\nexit 0\n')
  (self.origin/'scripts/deploy-profile.sh').write_text("APP_ID=fixture\nSOURCE_SUBDIR=.\nDEFAULT_DESTINATION=''\nPUBLIC_FILES=$'app.js\\nindex.html\\nsw.js'\n")
  (self.origin/'scripts/deploy.sh').write_text('''#!/bin/bash
set -euo pipefail
DEPLOY_CHECKOUT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
source "$DEPLOY_CHECKOUT/scripts/deploy-profile.sh"
source "$DEPLOY_CHECKOUT/scripts/deploy-core.sh"
deploy_main "$@"
''')
  for f in ['app.js','index.html','sw.js']:(self.origin/f).write_text('new '+f);(self.site/f).write_text('old '+f)
  (self.site/'unrelated.txt').write_text('keep');self.commit();self.git('clone',str(self.origin),str(self.repo))
 def git(self,*args):return subprocess.run(['git',*args],capture_output=True,text=True,check=True)
 def commit(self):self.git('-C',str(self.origin),'add','-A');self.git('-C',str(self.origin),'commit','-m','fixture')
 def run_deploy(self,*args):return subprocess.run(['/bin/bash',str(self.repo/'scripts/deploy.sh'),*args,str(self.site)],capture_output=True,text=True)
 def unchanged(self):self.assertEqual((self.site/'index.html').read_text(),'old index.html')
 def test_publishes_only_allowlist(self):
  r=self.run_deploy();self.assertEqual(r.returncode,0,r.stderr);self.assertEqual((self.site/'index.html').read_text(),'new index.html');self.assertEqual((self.site/'unrelated.txt').read_text(),'keep');self.assertFalse((self.site/'scripts').exists())
 def test_dry_run_is_read_only(self):
  before=self.git('-C',str(self.repo),'rev-parse','HEAD').stdout;r=self.run_deploy('--dry-run');self.assertEqual(r.returncode,0,r.stderr);self.unchanged();self.assertEqual(before,self.git('-C',str(self.repo),'rev-parse','HEAD').stdout);self.assertEqual(set(p.name for p in self.site.iterdir()),{'app.js','index.html','sw.js','unrelated.txt'})
 def test_failed_pull_aborts(self):
  shutil.rmtree(self.origin);r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.unchanged()
 def test_dirty_checkout_aborts(self):
  (self.repo/'app.js').write_text('uncommitted');r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.unchanged()
 def test_local_only_commit_aborts(self):
  self.git('-C',str(self.repo),'config','user.email','test@example.invalid');self.git('-C',str(self.repo),'config','user.name','Test');(self.repo/'app.js').write_text('local');self.git('-C',str(self.repo),'add','app.js');self.git('-C',str(self.repo),'commit','-m','local');r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.unchanged()
 def test_nested_destination_symlink_aborts(self):
  other=self.root/'other';other.mkdir();(self.site/'app.js').unlink();(self.site/'app.js').symlink_to(other/'escaped');r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.unchanged();self.assertFalse((other/'escaped').exists())
 def test_source_overlap_aborts(self):
  self.site=self.repo;r=self.run_deploy();self.assertNotEqual(r.returncode,0)
 def test_traversal_manifest_aborts(self):
  p=self.origin/'scripts/deploy-profile.sh';p.write_text(p.read_text()+"\nPUBLIC_FILES=$'../escape\\nindex.html'\n");self.commit();self.git('-C',str(self.repo),'pull','--ff-only');r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.assertIn('Unsafe public path',r.stderr);self.unchanged()
 def test_existing_lock_preserved(self):
  lock=self.site/'.basecentral-deploy.lock';lock.mkdir();r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.assertTrue(lock.exists());self.unchanged()
 def test_missing_asset_preserves_whole_site(self):
  self.git('-C',str(self.origin),'rm','sw.js');self.commit();r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.unchanged()

 def profile(self, extra):
  p=self.origin/'scripts/deploy-profile.sh';p.write_text(p.read_text()+extra);self.commit();self.git('-C',str(self.repo),'pull','--ff-only')
 def test_release_directory_is_publicly_traversable(self):
  app=self.root/'app';releases=app/'releases';old=releases/'old';(old/'web').mkdir(parents=True);(old/'web/index.html').write_text('old release');current=app/'current';current.symlink_to(old,target_is_directory=True);self.site=current
  self.profile('\nDEPLOY_MODE=release\nRELEASE_ROOT="'+str(releases)+'"\n')
  r=self.run_deploy();self.assertEqual(r.returncode,0,r.stderr);self.assertEqual((current/'web/index.html').read_text(),'new index.html');self.assertEqual(current.resolve().stat().st_mode & 0o777,0o755)
 def test_legacy_balance_dry_run_env_cannot_publish(self):
  env=dict(os.environ,BALANCE_DRY_RUN='1');r=subprocess.run(['/bin/bash',str(self.repo/'scripts/deploy.sh'),str(self.site)],env=env,capture_output=True,text=True);self.assertEqual(r.returncode,0,r.stderr);self.unchanged()
 def test_nested_root_alias_rejected(self):
  outside=self.root/'outside';outside.mkdir();public=outside/'public';public.mkdir();(public/'index.html').write_text('sentinel');alias=self.root/'alias';alias.symlink_to(outside,target_is_directory=True);self.site=alias/'public'
  r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.assertEqual((public/'index.html').read_text(),'sentinel')


 def test_failed_staging_preserves_public_files_and_cleans_lock(self):
  self.profile('\ndeploy_prepare(){ return 7; }\n');r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.unchanged();self.assertFalse((self.site/'.basecentral-deploy.lock').exists());self.assertFalse(list(self.site.glob('.basecentral-stage.*')))
 def test_source_change_during_staging_aborts(self):
  self.profile('\ndeploy_prepare(){ printf changed >> "$DEPLOY_CHECKOUT/app.js"; }\n');r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.unchanged()
 def test_backup_root_alias_rejected(self):
  actual=self.root/'private';actual.mkdir();alias=self.root/'backup-alias';alias.symlink_to(actual,target_is_directory=True);self.profile('\nBACKUP_ROOT="'+str(alias/'backups')+'"\n');r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.unchanged();self.assertFalse((actual/'backups').exists())
 def test_release_activation_failure_retains_previous_link(self):
  app=self.root/'app';releases=app/'releases';old=releases/'old';(old/'web').mkdir(parents=True);(old/'web/index.html').write_text('old release');current=app/'current';current.symlink_to(old,target_is_directory=True);self.site=current
  self.profile('\nDEPLOY_MODE=release\nRELEASE_ROOT="'+str(releases)+'"\nmv(){ case \"$1\" in -fh|-fT) return 9;; *) command mv \"$@\";; esac; }\n')
  r=self.run_deploy();self.assertNotEqual(r.returncode,0);self.assertEqual(current.resolve(),old.resolve());self.assertEqual((current/'web/index.html').read_text(),'old release')

if __name__=='__main__':unittest.main()
