"""Exercise deployment against disposable local Git repositories; no network."""
import pathlib
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).with_name("deploy.sh")
ASSETS = ("index.html", "styles.css", "favicon.svg")


class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pwa-deploy-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.source = self.root / "source"
        self.checkout = self.root / "host checkout"
        self.web = self.root / "public site"
        self.web.mkdir()
        self.git("init", "--initial-branch=main", str(self.source))
        self.git("-C", str(self.source), "config", "user.name", "Deployment test")
        self.git("-C", str(self.source), "config", "user.email", "deploy-test@example.invalid")
        (self.source / "scripts").mkdir()
        self.assertTrue(SCRIPT.is_file(), "deployment script is not implemented")
        shutil.copyfile(SCRIPT, self.source / "scripts/deploy.sh")
        for name in ASSETS:
            (self.source / name).write_text("initial " + name)
            (self.web / name).write_text("published " + name)
        (self.source / "README.md").write_text("not public")
        self.commit("initial")
        self.git("clone", str(self.source), str(self.checkout))
        self.git("-C", str(self.checkout), "config", "user.name", "Deployment test")
        self.git("-C", str(self.checkout), "config", "user.email", "deploy-test@example.invalid")

    def git(self, *args):
        return subprocess.run(["git", *args], check=True, capture_output=True, text=True)

    def commit(self, message):
        self.git("-C", str(self.source), "add", "-A")
        self.git("-C", str(self.source), "commit", "-m", message)

    def deploy(self, target=None):
        return subprocess.run(["sh", str(self.checkout / "scripts/deploy.sh"),
                               str(target or self.web)], cwd=self.root,
                              capture_output=True, text=True)

    def assert_unpublished(self):
        for name in ASSETS:
            self.assertEqual((self.web / name).read_text(), "published " + name)

    def test_pulls_and_publishes_only_assets_preserving_other_host_files(self):
        for name in ASSETS:
            (self.source / name).write_text("new " + name)
        self.commit("new assets")
        (self.web / ".htaccess").write_text("host configuration")
        result = self.deploy()
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ASSETS:
            self.assertEqual((self.web / name).read_text(), "new " + name)
        self.assertEqual((self.web / ".htaccess").read_text(), "host configuration")
        self.assertEqual(set(p.name for p in self.web.iterdir()), {*ASSETS, ".htaccess"})

    def test_dirty_checkout_does_not_publish(self):
        (self.checkout / "index.html").write_text("local edit")
        result = self.deploy()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("clean", result.stderr)
        self.assert_unpublished()

    def test_divergent_history_does_not_publish(self):
        (self.source / "README.md").write_text("remote change")
        self.commit("remote change")
        (self.checkout / "README.md").write_text("host change")
        self.git("-C", str(self.checkout), "add", "README.md")
        self.git("-C", str(self.checkout), "commit", "-m", "host change")
        self.assertNotEqual(self.deploy().returncode, 0)
        self.assert_unpublished()

    def test_missing_asset_after_pull_does_not_publish(self):
        (self.source / "styles.css").unlink()
        self.commit("missing asset")
        result = self.deploy()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("styles.css", result.stderr)
        self.assert_unpublished()

    def test_host_only_commit_does_not_publish(self):
        (self.checkout / "index.html").write_text("host-only change")
        self.git("-C", str(self.checkout), "add", "index.html")
        self.git("-C", str(self.checkout), "commit", "-m", "host-only change")
        self.assertNotEqual(self.deploy().returncode, 0)
        self.assert_unpublished()

    def test_public_directory_cannot_be_inside_checkout(self):
        target = self.checkout / "public"
        target.mkdir()
        result = self.deploy(target)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(target.iterdir()), [])

    def test_symlink_target_does_not_overwrite_external_file(self):
        external = self.root / "outside.txt"
        external.write_text("untouched")
        (self.web / "index.html").unlink()
        (self.web / "index.html").symlink_to(external)
        self.assertNotEqual(self.deploy().returncode, 0)
        self.assertEqual(external.read_text(), "untouched")


if __name__ == "__main__":
    unittest.main(verbosity=2)
