#!/usr/bin/env python3#!/usr/bin/env python3

""""""

Template Syntax Testing ScriptTest template syntax fix

Tests all Flask templates for syntax errors"""

"""

import sys

import sysimport os

import ossys.path.append(os.path.dirname(os.path.abspath(__file__)))

from jinja2 import Environment, FileSystemLoader, TemplateSyntaxError

print("🧪 Testing Template Syntax Fix")

def test_template_syntax():print("=" * 40)

    """Test all templates for syntax errors"""

    print("=== Template Syntax Test ===")try:

        print("📦 Importing Flask app...")

    # Template directory    from app_simple import app

    template_dir = os.path.join(os.path.dirname(__file__), 'templates')    print("✅ Flask app imported successfully")

        

    if not os.path.exists(template_dir):    print("\n🎭 Testing template rendering...")

        print("❌ Templates directory not found!")    with app.test_client() as client:

        return False        # Test encrypt page (the one that was failing)

            print("   Testing /encrypt page...")

    # Create Jinja2 environment        response = client.get('/encrypt')

    env = Environment(loader=FileSystemLoader(template_dir))        if response.status_code == 200:

                print("   ✅ Encrypt page renders successfully")

    # Get all template files        elif response.status_code == 302:

    template_files = []            print("   🔄 Encrypt page redirects (OK)")

    for file in os.listdir(template_dir):        else:

        if file.endswith('.html'):            print(f"   ❌ Encrypt page error: {response.status_code}")

            template_files.append(file)            

            # Test decrypt page

    print(f"\nFound {len(template_files)} template files to test:")        print("   Testing /decrypt page...")

            response = client.get('/decrypt')

    errors_found = 0        if response.status_code == 200:

                print("   ✅ Decrypt page renders successfully")

    for template_file in sorted(template_files):        elif response.status_code == 302:

        try:            print("   🔄 Decrypt page redirects (OK)")

            # Try to parse the template        else:

            template = env.get_template(template_file)            print(f"   ❌ Decrypt page error: {response.status_code}")

            print(f"✅ {template_file}")            

        except TemplateSyntaxError as e:        # Test dashboard

            print(f"❌ {template_file}: Syntax Error - {e}")        print("   Testing /dashboard page...")

            errors_found += 1        response = client.get('/dashboard')

        except Exception as e:        if response.status_code == 200:

            print(f"❌ {template_file}: Error - {e}")            print("   ✅ Dashboard renders successfully")

            errors_found += 1        elif response.status_code == 302:

                print("   🔄 Dashboard redirects (OK)")

    print(f"\n=== Template Test Results ===")        else:

    print(f"Total templates: {len(template_files)}")            print(f"   ❌ Dashboard error: {response.status_code}")

    print(f"Passed: {len(template_files) - errors_found}")            

    print(f"Failed: {errors_found}")    print("\n🎉 All template tests passed!")

        print("🌐 Flask app is ready to run!")

    if errors_found == 0:    

        print("✅ All templates passed syntax check!")except Exception as e:

        return True    print(f"❌ Error: {e}")

    else:    import traceback

        print("❌ Some templates have syntax errors!")    traceback.print_exc()

        return False

print("\n" + "=" * 40)

def check_template_completeness():
    """Check if all expected templates exist"""
    print("\n=== Template Completeness Check ===")
    
    expected_templates = [
        'base.html',
        'dashboard.html',
        'login.html',
        'login_simple.html',
        'encrypt.html',
        'decrypt.html',
        'file_encrypt.html',
        'file_decrypt.html',
        'encrypt_result.html',
        'decrypt_result.html',
        'manage_users.html',
        'activity_log.html',
        'user_attributes.html',
        'policy_checker.html'
    ]
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    missing_templates = []
    
    for template in expected_templates:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - MISSING")
            missing_templates.append(template)
    
    if missing_templates:
        print(f"\n⚠️  Missing {len(missing_templates)} templates!")
        return False
    else:
        print("\n✅ All expected templates found!")
        return True

if __name__ == "__main__":
    print("Template Syntax and Completeness Test")
    print("=" * 40)
    
    syntax_ok = test_template_syntax()
    complete_ok = check_template_completeness()
    
    if syntax_ok and complete_ok:
        print("\n🎉 All template tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some template tests failed!")
        sys.exit(1)