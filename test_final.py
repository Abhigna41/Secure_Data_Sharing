#!/usr/bin/env python3#!/usr/bin/env python3

""""""

Final Testing SuiteFinal test script to verify all pages and functionality work correctly

Comprehensive final testing before deploymentwith the new clean theme.

""""""



import sysimport subprocess

import osimport time

import subprocessimport requests

import timeimport sys

import os

def run_test_file(test_file):

    """Run a specific test file and return result"""def test_flask_app():

    try:    """Test the Flask application endpoints"""

        print(f"\n🧪 Running {test_file}...")    

        result = subprocess.run([sys.executable, test_file],     print("🚀 Starting Flask app test...")

                              capture_output=True, text=True, timeout=30)    

            # Start Flask app in background

        if result.returncode == 0:    app_process = None

            print(f"✅ {test_file} - PASSED")    try:

            return True        app_process = subprocess.Popen([

        else:            sys.executable, "app_simple.py"

            print(f"❌ {test_file} - FAILED")        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if result.stderr:        

                print(f"   Error: {result.stderr.strip()}")        # Wait for app to start

            return False        time.sleep(3)

                    

    except subprocess.TimeoutExpired:        base_url = "http://localhost:5000"

        print(f"⏰ {test_file} - TIMEOUT")        

        return False        # Test pages that should be accessible

    except Exception as e:        test_pages = [

        print(f"❌ {test_file} - ERROR: {e}")            "/",

        return False            "/login",

            "/login_simple",

def test_final():        ]

    """Run final testing suite"""        

    print("=== Final Testing Suite ===")        print("\n📋 Testing page accessibility...")

    print("Comprehensive testing before deployment")        for page in test_pages:

    print()            try:

                    response = requests.get(f"{base_url}{page}", timeout=5)

    # Test files to run                status = "✅ OK" if response.status_code == 200 else f"❌ {response.status_code}"

    test_files = [                print(f"  {page}: {status}")

        'startup_test.py',            except Exception as e:

        'template_syntax_test.py',                print(f"  {page}: ❌ Error - {str(e)}")

        'quick_template_test.py',        

        'test_abe_policy.py'        # Test guest login

    ]        print("\n🔑 Testing guest login...")

            try:

    # Check which test files exist            response = requests.post(f"{base_url}/guest_login", timeout=5)

    available_tests = []            if response.status_code in [200, 302]:  # 302 for redirect

    for test_file in test_files:                print("  Guest login: ✅ OK")

        if os.path.exists(test_file):            else:

            available_tests.append(test_file)                print(f"  Guest login: ❌ {response.status_code}")

        else:        except Exception as e:

            print(f"⚠️  {test_file} not found - skipping")            print(f"  Guest login: ❌ Error - {str(e)}")

            

    if not available_tests:        print("\n✨ All tests completed!")

        print("❌ No test files found!")        

        return False    except Exception as e:

            print(f"❌ Error starting app: {e}")

    print(f"\nRunning {len(available_tests)} test suites...")    

        finally:

    # Run tests        if app_process:

    passed_tests = 0            app_process.terminate()

    for test_file in available_tests:            try:

        if run_test_file(test_file):                app_process.wait(timeout=5)

            passed_tests += 1            except subprocess.TimeoutExpired:

                    app_process.kill()

    # Summary

    total_tests = len(available_tests)def check_template_consistency():

    print(f"\n=== Final Test Results ===")    """Check that all templates use consistent styling"""

    print(f"Total Test Suites: {total_tests}")    

    print(f"Passed: {passed_tests}")    print("\n🎨 Checking template consistency...")

    print(f"Failed: {total_tests - passed_tests}")    

    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")    template_dir = "templates"

        templates = [f for f in os.listdir(template_dir) if f.endswith('.html')]

    if passed_tests == total_tests:    

        print("\n🎉 All tests passed!")    issues = []

        print("✅ Application is ready for deployment!")    

        return True    for template in templates:

    else:        template_path = os.path.join(template_dir, template)

        print(f"\n❌ {total_tests - passed_tests} test suites failed!")        try:

        print("🔧 Please fix the issues before deployment")            with open(template_path, 'r', encoding='utf-8') as f:

        return False                content = f.read()

                

def check_system_readiness():                # Check for vibrant colors that should be removed

    """Check if system is ready for testing"""                vibrant_patterns = [

    print("=== System Readiness Check ===")                    'gradient', 'linear-gradient', 'radial-gradient',

                        'orange', '#ff', '#f39c12', '#e67e22',

    # Check Python version                    'rgba(255,', 'rgba(243,', 'rgba(230,'

    python_version = sys.version_info                ]

    if python_version >= (3, 6):                

        print(f"✅ Python version: {python_version.major}.{python_version.minor}")                for pattern in vibrant_patterns:

    else:                    if pattern.lower() in content.lower():

        print(f"❌ Python version too old: {python_version.major}.{python_version.minor}")                        issues.append(f"{template}: Contains '{pattern}'")

        return False                

                    # Check for proper extends

    # Check current directory                if template not in ['base.html'] and 'extends "base.html"' not in content:

    current_dir = os.getcwd()                    if 'extends "encrypt_result.html"' not in content:  # decrypt_result is ok

    if 'Secure_Data_Sharing' in current_dir:                        issues.append(f"{template}: Should extend base.html")

        print(f"✅ Working directory: {os.path.basename(current_dir)}")        

    else:        except Exception as e:

        print(f"⚠️  Working directory: {os.path.basename(current_dir)}")            issues.append(f"{template}: Error reading - {str(e)}")

        

    # Check for main application file    if issues:

    if os.path.exists('app_simple.py'):        print("❌ Template issues found:")

        print("✅ Main application file found")        for issue in issues:

    else:            print(f"  - {issue}")

        print("❌ Main application file not found")    else:

        return False        print("✅ All templates look consistent!")

    

    # Check for templates directoryif __name__ == "__main__":

    if os.path.exists('templates'):    print("🧪 Final Testing Suite - Clean Theme Verification")

        template_count = len([f for f in os.listdir('templates') if f.endswith('.html')])    print("=" * 60)

        print(f"✅ Templates directory found ({template_count} files)")    

    else:    # Change to correct directory

        print("❌ Templates directory not found")    script_dir = os.path.dirname(os.path.abspath(__file__))

        return False    os.chdir(script_dir)

        

    print("✅ System readiness check passed")    check_template_consistency()

    return True    test_flask_app()

    

if __name__ == "__main__":    print("\n🎉 Testing complete!")

    print("Secure Data Sharing System - Final Testing Suite")    print("\nTo manually test the app:")

    print("=" * 55)    print("1. Run: python app_simple.py")

    print()    print("2. Open: http://localhost:5000")

        print("3. Try both admin login and guest login tabs")

    # Check system readiness first    print("4. Navigate through all pages to verify clean styling")

    if not check_system_readiness():
        print("\n❌ System not ready for testing!")
        sys.exit(1)
    
    # Run final tests
    success = test_final()
    
    if success:
        print("\n🚀 System is ready for production!")
    else:
        print("\n🔧 Please address the test failures")
    
    sys.exit(0 if success else 1)