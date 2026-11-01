"""Directory generator behavior with synthetic sibling apps; no network."""
import importlib.util,json,pathlib,subprocess,tempfile,unittest
SCRIPT=pathlib.Path(__file__).resolve().parents[1]/'scripts/build-directory.py'
class DirectoryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='directory-');self.addCleanup(self.tmp.cleanup);self.root=pathlib.Path(self.tmp.name);self.site=self.root/'pwa';self.site.mkdir();self.config=self.site/'apps.txt'
  for folder,name,domain in [('one','First app','one.example.test'),('two','Second app','two.example.test')]:
   app=self.root/folder;(app/'scripts').mkdir(parents=True);(app/'manifest.webmanifest').write_text(json.dumps({'name':name,'description':'Useful things, locally.','icons':[{'src':'icon.svg','type':'image/svg+xml'}]}));(app/'scripts/deploy-profile.sh').write_text('SOURCE_SUBDIR=.\nDEPLOY_URL=https://'+domain+'\n');(app/'README.md').write_text('# '+name+'\n\nUseful things, locally.\n')
 def run_build(self):return subprocess.run(['python3',str(SCRIPT),'--root',str(self.root),'--site',str(self.site)],capture_output=True,text=True)
 def test_folder_list_alone_controls_links_and_order(self):
  self.config.write_text('# Display order\ntwo\none\n');r=self.run_build();self.assertEqual(r.returncode,0,r.stderr);html=(self.site/'index.html').read_text();self.assertLess(html.index('Second app'),html.index('First app'));self.assertIn('https://two.example.test/',html);self.assertIn('referrerpolicy="no-referrer"',html)
  self.config.write_text('one\n');r=self.run_build();self.assertEqual(r.returncode,0,r.stderr);self.assertNotIn('Second app',(self.site/'index.html').read_text())
 def test_app_metadata_changes_need_no_directory_mapping(self):
  self.config.write_text('one\n');manifest=self.root/'one/manifest.webmanifest';data=json.loads(manifest.read_text());data['name']='New <name>';manifest.write_text(json.dumps(data));r=self.run_build();self.assertEqual(r.returncode,0,r.stderr);self.assertIn('New &lt;name&gt;',(self.site/'index.html').read_text());self.assertNotIn('New <name>',(self.site/'index.html').read_text())
 def test_bad_folder_preserves_previous_generated_page(self):
  (self.site/'index.html').write_text('previous');self.config.write_text('../secret\n');r=self.run_build();self.assertNotEqual(r.returncode,0);self.assertEqual((self.site/'index.html').read_text(),'previous')
 def test_unknown_url_is_not_invented(self):
  self.config.write_text('one\n');(self.root/'one/scripts/deploy-profile.sh').write_text('SOURCE_SUBDIR=.\n');r=self.run_build();self.assertNotEqual(r.returncode,0);self.assertIn('URL',r.stderr)
 def test_duplicate_folders_rejected(self):
  self.config.write_text('one\none\n');r=self.run_build();self.assertNotEqual(r.returncode,0);self.assertIn('duplicate',r.stderr.lower())

 def test_documented_url_preserves_hosting_subdirectory(self):
  self.config.write_text('one\n');(self.root/'one/scripts/deploy-profile.sh').write_text('SOURCE_SUBDIR=.\n');(self.root/'one/README.md').write_text('# App\n\nProduction URL: https://demo.basecentral.link/my-app/\n');r=self.run_build();self.assertEqual(r.returncode,0,r.stderr);self.assertIn('href="https://demo.basecentral.link/my-app/"',(self.site/'index.html').read_text())
 def test_invalid_port_preserves_previous_page(self):
  for url in ['https://example.test:garbage/','https://example.test:99999/','https://[broken/']:
   with self.subTest(url=url):
    self.config.write_text('one\n');(self.site/'index.html').write_text('previous');(self.root/'one/scripts/deploy-profile.sh').write_text('SOURCE_SUBDIR=.\nDEPLOY_URL='+url+'\n');r=self.run_build();self.assertNotEqual(r.returncode,0);self.assertIn('Directory build stopped',r.stderr);self.assertNotIn('Traceback',r.stderr);self.assertEqual((self.site/'index.html').read_text(),'previous')
 def test_empty_list_removes_all_app_links(self):
  self.config.write_text('# No selected apps\n');r=self.run_build();self.assertEqual(r.returncode,0,r.stderr);html=(self.site/'index.html').read_text();self.assertNotIn('class="app-link"',html);self.assertIn('No apps are listed',html)

if __name__=='__main__':unittest.main()
