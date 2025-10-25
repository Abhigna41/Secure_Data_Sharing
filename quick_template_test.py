#!/usr/bin/env python3#!/usr/bin/env python3

""""""

Quick Template Testing ScriptSimple template syntax test

Fast testing of template syntax and loading"""

"""

try:

import os    print("Testing Flask app import...")

import sys    from app_simple import app

    print("✅ Flask app imported successfully")

def quick_template_test():    

    """Quick test of template files"""    print("Testing template rendering...")

    print("=== Quick Template Test ===")    with app.test_client() as client:

            response = client.get('/')

    template_dir = os.path.join(os.path.dirname(__file__), 'templates')        if response.status_code == 200:

                print("✅ Home page renders without errors")

    if not os.path.exists(template_dir):        elif response.status_code == 302:

        print("❌ Templates directory not found!")            print("✅ Home page redirects (OK)")

        return False        else:

                print(f"⚠️ Home page returned status {response.status_code}")

    # Get all HTML files            

    html_files = [f for f in os.listdir(template_dir) if f.endswith('.html')]        response = client.get('/dashboard')

            if response.status_code == 200:

    print(f"\nFound {len(html_files)} template files:")            print("✅ Dashboard renders without errors")

            elif response.status_code == 302:

    for html_file in sorted(html_files):            print("✅ Dashboard redirects (OK)")

        file_path = os.path.join(template_dir, html_file)        else:

        try:            print(f"⚠️ Dashboard returned status {response.status_code}")

            with open(file_path, 'r', encoding='utf-8') as f:            

                content = f.read()except Exception as e:

                    print(f"❌ Error: {e}")

            # Basic checks    import traceback

            has_html_tag = '<html>' in content or '<!DOCTYPE html>' in content or '{% extends' in content    traceback.print_exc()

            has_closing_tags = content.count('<') <= content.count('>')

            print("Template test completed!")

            if has_html_tag or '{% extends' in content:
                print(f"✅ {html_file}")
            else:
                print(f"⚠️  {html_file} - May be incomplete")
                
        except Exception as e:
            print(f"❌ {html_file} - Error reading: {e}")
    
    print(f"\n✅ Quick template test complete!")
    return True

if __name__ == "__main__":
    quick_template_test()