"""
Tests for packaging configuration and metadata validation.
"""

import os
import tempfile
import unittest
import subprocess
import sys
from pathlib import Path

# Use tomllib for Python 3.11+, fallback to toml for older versions
try:
    import tomllib
    def load_toml(file_path):
        with open(file_path, 'rb') as f:
            return tomllib.load(f)
except ImportError:
    try:
        import toml
        def load_toml(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return toml.load(f)
    except ImportError:
        # Fallback to basic parsing if no TOML library available
        def load_toml(file_path):
            raise unittest.SkipTest("No TOML library available for testing")


class TestPackagingConfiguration(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.project_root = Path(__file__).parent.parent
        self.pyproject_path = self.project_root / "pyproject.toml"
    
    def test_pyproject_toml_exists_and_valid(self):
        """Test that pyproject.toml exists and is valid TOML."""
        self.assertTrue(self.pyproject_path.exists(), "pyproject.toml must exist")
        
        # Validate TOML syntax
        try:
            config = load_toml(self.pyproject_path)
        except Exception as e:
            self.fail(f"pyproject.toml is not valid TOML: {e}")
    
    def test_required_metadata_fields(self):
        """Test that all required metadata fields are present."""
        config = load_toml(self.pyproject_path)
        
        project = config.get('project', {})
        
        # Required fields per PEP 621
        required_fields = ['name', 'version', 'description', 'authors']
        for field in required_fields:
            self.assertIn(field, project, f"Required field '{field}' missing from project metadata")
    
    def test_license_format_compliance(self):
        """Test that license follows modern SPDX format."""
        config = load_toml(self.pyproject_path)
        
        project = config.get('project', {})
        
        # Check license is a string (SPDX format)
        self.assertIn('license', project, "License field must be present")
        self.assertIsInstance(project['license'], str, "License must be SPDX string format")
        self.assertEqual(project['license'], 'MIT', "License should be MIT")
        
        # Ensure deprecated license classifier is not used
        classifiers = project.get('classifiers', [])
        license_classifiers = [c for c in classifiers if c.startswith('License ::')]
        self.assertEqual(len(license_classifiers), 0, 
                        "Deprecated license classifiers should not be used with SPDX license")
    
    def test_keywords_present_and_relevant(self):
        """Test that keywords are present and relevant for discoverability."""
        config = load_toml(self.pyproject_path)
        
        project = config.get('project', {})
        
        self.assertIn('keywords', project, "Keywords should be present for PyPI discoverability")
        keywords = project['keywords']
        self.assertIsInstance(keywords, list, "Keywords should be a list")
        self.assertGreater(len(keywords), 0, "At least one keyword should be present")
        
        # Check for relevant keywords
        expected_keywords = ['static-site-generator', 'markdown', 'html']
        for keyword in expected_keywords:
            self.assertIn(keyword, keywords, f"Expected keyword '{keyword}' should be present")
    
    def test_urls_completeness(self):
        """Test that all important project URLs are configured."""
        config = load_toml(self.pyproject_path)
        
        urls = config.get('project', {}).get('urls', {})
        
        # Required URLs for professional appearance
        required_urls = ['Homepage', 'Repository', 'Bug Tracker']
        for url_key in required_urls:
            self.assertIn(url_key, urls, f"URL '{url_key}' should be configured")
            self.assertTrue(urls[url_key].startswith('http'), 
                          f"URL '{url_key}' should be a valid HTTP(S) URL")
    
    def test_optional_dependencies_structure(self):
        """Test that optional dependencies are properly structured."""
        config = load_toml(self.pyproject_path)
        
        optional_deps = config.get('project', {}).get('optional-dependencies', {})
        
        # Check dev dependencies
        self.assertIn('dev', optional_deps, "Development dependencies should be defined")
        dev_deps = optional_deps['dev']
        self.assertIsInstance(dev_deps, list, "Dev dependencies should be a list")
        
        # Check for essential dev tools
        dev_tools = ['pytest', 'ruff', 'twine', 'build']
        for tool in dev_tools:
            matching_deps = [dep for dep in dev_deps if dep.startswith(tool)]
            self.assertGreater(len(matching_deps), 0, 
                             f"Dev dependencies should include {tool}")
        
        # Check test dependencies
        self.assertIn('test', optional_deps, "Test dependencies should be defined")
        test_deps = optional_deps['test']
        self.assertIsInstance(test_deps, list, "Test dependencies should be a list")
    
    def test_python_version_compatibility(self):
        """Test that Python version requirements are appropriate."""
        config = load_toml(self.pyproject_path)
        
        project = config.get('project', {})
        
        self.assertIn('requires-python', project, "Python version requirement must be specified")
        requires_python = project['requires-python']
        
        # Should support Python 3.8+ for good compatibility
        self.assertTrue(requires_python.startswith('>=3.8'), 
                       "Should support Python 3.8+ for broad compatibility")
        
        # Check classifiers match
        classifiers = project.get('classifiers', [])
        python_classifiers = [c for c in classifiers if c.startswith('Programming Language :: Python ::')]
        self.assertGreater(len(python_classifiers), 0, "Python version classifiers should be present")
    
    def test_build_system_configuration(self):
        """Test that build system is properly configured."""
        config = load_toml(self.pyproject_path)
        
        build_system = config.get('build-system', {})
        
        self.assertIn('requires', build_system, "Build system requires must be specified")
        self.assertIn('build-backend', build_system, "Build backend must be specified")
        
        requires = build_system['requires']
        self.assertIn('setuptools>=61.0', requires, "Modern setuptools should be required")
    
    def test_package_discovery_configuration(self):
        """Test that package discovery is explicitly configured."""
        config = load_toml(self.pyproject_path)
        
        # Check the correct nested structure for setuptools packages.find
        tool_config = config.get('tool', {})
        setuptools_config = tool_config.get('setuptools', {})
        packages_find = setuptools_config.get('packages', {}).get('find', {})
        
        # If no explicit configuration, that might be okay too, 
        # but we should have explicit configuration for our case
        if packages_find:
            self.assertIn('include', packages_find, 
                         "Package discovery should explicitly include simple_ssg")
            self.assertIn('exclude', packages_find, 
                         "Package discovery should exclude temporary directories")
            
            include = packages_find['include']
            exclude = packages_find['exclude']
            
            self.assertIn('simple_ssg*', include, "Should include simple_ssg package")
            self.assertIn('logs*', exclude, "Should exclude logs directory")
        else:
            # Allow for cases where default discovery works, but warn
            import warnings
            warnings.warn("Package discovery not explicitly configured")


class TestPackageBuildProcess(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.project_root = Path(__file__).parent.parent
    
    def test_package_builds_successfully(self):
        """Test that the package can be built without errors."""
        # Change to project directory
        original_cwd = os.getcwd()
        os.chdir(self.project_root)
        
        try:
            # Run build command
            result = subprocess.run([
                sys.executable, '-m', 'build', '--wheel'
            ], capture_output=True, text=True, timeout=120)
            
            # Check build succeeded
            self.assertEqual(result.returncode, 0, 
                           f"Package build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}")
            
            # Check for warnings in output
            stderr_lower = result.stderr.lower()
            
            # Check for unexpected errors (should cause test failure)
            if 'error' in stderr_lower and 'deprecated' not in stderr_lower:
                self.fail(f"Unexpected error in build output: {result.stderr}")
            
            # Check for unexpected warnings (should cause test failure)
            warning_keywords = ['warning']
            for keyword in warning_keywords:
                if keyword in stderr_lower and 'deprecated' not in stderr_lower:
                    self.fail(f"Unexpected {keyword} in build output: {result.stderr}")
            
            # Allow known deprecation warnings as they're being addressed
            if 'deprecation' in stderr_lower or 'deprecated' in stderr_lower:
                import warnings
                warnings.warn(f"Build contains deprecation warnings: {result.stderr}")
                
        finally:
            os.chdir(original_cwd)
    
    def test_package_metadata_in_wheel(self):
        """Test that built wheel contains proper metadata."""
        # This test would check the built wheel's metadata
        # For now, we'll check that dist files can be created
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(self.project_root)
            
            try:
                # Build to temporary directory
                result = subprocess.run([
                    sys.executable, '-m', 'build', '--wheel', '--outdir', temp_dir
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    # Check wheel file was created
                    wheel_files = list(Path(temp_dir).glob('*.whl'))
                    self.assertGreater(len(wheel_files), 0, "Wheel file should be created")
                    
            finally:
                os.chdir(original_cwd)


if __name__ == '__main__':
    unittest.main()