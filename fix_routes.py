#!/usr/bin/env python3
"""
Fix template routes from blueprint style to simple function names
"""

import os
import re

# Mapping from blueprint routes to simple function names
route_mappings = {
    # Auth routes
    'auth.guest_login': 'guest_login',
    'auth.logout': 'logout',
    
    # Main routes
    'main.dashboard': 'dashboard',
    'main.manage_users': 'manage_users',
    'main.activity_log': 'view_activity_log',
    'main.user_attributes': 'user_attributes',
    'main.policy_checker': 'policy_checker',
    
    # Data routes
    'data.encrypt': 'encrypt_data',
    'data.decrypt': 'decrypt_data',
    
    # File routes
    'files.encrypt': 'file_encrypt',
    'files.decrypt': 'file_decrypt',
    'files.download': 'download_file',
}

def fix_template_file(filepath):
    """Fix blueprint routes in a single template file"""
    print(f"Fixing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace each blueprint route with simple function name
    for blueprint_route, simple_route in route_mappings.items():
        pattern = f"url_for\\('{blueprint_route}'\\)"
        replacement = f"url_for('{simple_route}')"
        content = re.sub(pattern, replacement, content)
    
    # Write back if changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated {filepath}")
        return True
    else:
        print(f"  - No changes needed in {filepath}")
        return False

def main():
    """Fix all template files"""
    templates_dir = 'templates'
    fixed_count = 0
    
    print("=== Fixing Template Routes ===")
    print()
    
    if not os.path.exists(templates_dir):
        print(f"Templates directory not found: {templates_dir}")
        return
    
    # Get all HTML files in templates directory
    template_files = []
    for file in os.listdir(templates_dir):
        if file.endswith('.html'):
            template_files.append(os.path.join(templates_dir, file))
    
    print(f"Found {len(template_files)} template files")
    print()
    
    for template_file in sorted(template_files):
        if fix_template_file(template_file):
            fixed_count += 1
    
    print()
    print(f"=== Summary ===")
    print(f"Fixed {fixed_count} template files")
    print("All blueprint routes have been converted to simple function names")

if __name__ == '__main__':
    main()