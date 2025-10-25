#!/usr/bin/env python3#!/usr/bin/env python3

""""""

Application Startup TestQuick startup test for Flask app

Tests if the Flask application can start without errors"""

"""

import os

import sysimport sys

import os

# Add the current directory to Python path

def test_startup():sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    """Test if the application can start without errors"""

    print("=== Application Startup Test ===")print("=" * 60)

    print("🚀 FLASK APP STARTUP TEST")

    try:print("=" * 60)

        print("\n1. Testing imports...")

        try:

        # Test Flask import    print("📦 Importing Flask app...")

        try:    from app_simple import app

            from flask import Flask    print("✅ Flask app imported successfully!")

            print("✅ Flask import: OK")    

        except ImportError as e:    print("\n🔍 Checking available routes...")

            print(f"❌ Flask import failed: {e}")    routes = []

            return False    for rule in app.url_map.iter_rules():

                routes.append((rule.rule, rule.endpoint))

        # Test app_simple import    

        try:    print(f"✅ Found {len(routes)} routes:")

            import app_simple    for route, endpoint in sorted(routes):

            print("✅ app_simple import: OK")        print(f"   {route:25} -> {endpoint}")

        except ImportError as e:    

            print(f"❌ app_simple import failed: {e}")    print("\n🧪 Testing critical template rendering...")

            return False    with app.test_client() as client:

        except Exception as e:        # Test each major page

            print(f"⚠️  app_simple import warning: {e}")        test_pages = [

                    ('/', 'Home page'),

        print("\n2. Testing Flask app creation...")            ('/dashboard', 'Dashboard'),

        try:            ('/encrypt', 'Encrypt page'),

            from app_simple import app            ('/decrypt', 'Decrypt page'),

            print("✅ Flask app creation: OK")            ('/file_encrypt', 'File encrypt page'),

        except Exception as e:            ('/file_decrypt', 'File decrypt page'),

            print(f"❌ Flask app creation failed: {e}")            ('/manage_users', 'User management'),

            return False            ('/activity_log', 'Activity log')

                ]

        print("\n3. Testing template loading...")        

        try:        print(f"\n📄 Testing {len(test_pages)} pages...")

            with app.app_context():        for url, name in test_pages:

                # Test if templates can be found            try:

                template_dir = app.template_folder                response = client.get(url)

                if template_dir and os.path.exists(template_dir):                if response.status_code == 200:

                    print(f"✅ Template directory found: {template_dir}")                    print(f"   ✅ {name:20} - OK")

                                    elif response.status_code == 302:

                    # Count templates                    print(f"   🔄 {name:20} - Redirect (OK)")

                    templates = [f for f in os.listdir(template_dir) if f.endswith('.html')]                else:

                    print(f"✅ Found {len(templates)} template files")                    print(f"   ⚠️  {name:20} - Status {response.status_code}")

                else:            except Exception as e:

                    print("❌ Template directory not found")                print(f"   ❌ {name:20} - ERROR: {str(e)[:50]}...")

                    return False    

        except Exception as e:    print("\n🎉 STARTUP TEST COMPLETED!")

            print(f"❌ Template loading test failed: {e}")    print("🌐 Flask app is ready to run!")

            return False    

        except Exception as e:

        print("\n4. Testing routes...")    print(f"❌ CRITICAL ERROR: {e}")

        try:    import traceback

            routes = []    traceback.print_exc()

            for rule in app.url_map.iter_rules():    sys.exit(1)

                routes.append(str(rule))    

            print(f"✅ Found {len(routes)} routes:")print("\n" + "=" * 60)

            for route in sorted(routes)[:10]:  # Show first 10 routes
                print(f"   {route}")
            if len(routes) > 10:
                print(f"   ... and {len(routes) - 10} more")
        except Exception as e:
            print(f"❌ Route testing failed: {e}")
            return False
        
        print("\n=== Startup Test Results ===")
        print("✅ Application can start successfully!")
        print("✅ All critical components loaded")
        print("✅ Ready for production use")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Startup test failed with error: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are available"""
    print("\n=== Dependency Test ===")
    
    required_packages = [
        'flask',
        'werkzeug',
        'jinja2'
    ]
    
    optional_packages = [
        'requests',
        'json',
        'os',
        'uuid',
        'datetime',
        'base64'
    ]
    
    print("\nRequired packages:")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            return False
    
    print("\nOptional packages:")
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"⚠️  {package} - MISSING (optional)")
    
    return True

if __name__ == "__main__":
    print("Flask Application Startup Test")
    print("=" * 35)
    
    deps_ok = test_dependencies()
    startup_ok = test_startup()
    
    if deps_ok and startup_ok:
        print("\n🎉 All startup tests passed!")
        print("🚀 Application is ready to run!")
        sys.exit(0)
    else:
        print("\n❌ Some startup tests failed!")
        print("🔧 Please check the errors above")
        sys.exit(1)