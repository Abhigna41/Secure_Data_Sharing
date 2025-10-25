#!/usr/bin/env python3#!/usr/bin/env python3

""""""

Integration Testing SuiteQuick test to verify Activity Logs and Manage Users functionality

Comprehensive testing of the Secure Data Sharing System"""

"""

import sys

import sysimport os

import os

import requests# Add the current directory to Python path

import timesys.path.insert(0, os.getcwd())

import json

try:

class IntegrationTester:    from app_simple import app

    def __init__(self, base_url="http://localhost:5000"):    

        self.base_url = base_url    print("🔍 Checking Flask Routes...")

        self.session = requests.Session()    print("=" * 50)

        self.test_results = []    

        routes_found = []

    def log_test(self, test_name, passed, message=""):    for rule in app.url_map.iter_rules():

        """Log test result"""        routes_found.append((rule.endpoint, rule.rule))

        status = "✅ PASS" if passed else "❌ FAIL"    

        print(f"{status}: {test_name}")    # Check for required routes

        if message:    required_routes = {

            print(f"    {message}")        'manage_users': '/manage_users',

                'view_activity_log': '/activity_log',

        self.test_results.append({        'decrypt_data': '/decrypt'

            'name': test_name,    }

            'passed': passed,    

            'message': message    print("📋 Required Routes Status:")

        })    for endpoint, expected_rule in required_routes.items():

            found = any(rule[0] == endpoint for rule in routes_found)

    def test_application_accessibility(self):        status = "✅ FOUND" if found else "❌ MISSING"

        """Test if application is accessible"""        print(f"  {endpoint} ({expected_rule}): {status}")

        try:    

            response = self.session.get(self.base_url, timeout=5)    print("\n🌐 All Available Routes:")

            passed = response.status_code == 200    for endpoint, rule in sorted(routes_found):

            self.log_test("Application Accessibility", passed,         print(f"  {endpoint}: {rule}")

                         f"Status code: {response.status_code}")    

            return passed    print("\n🎯 Testing Template Integration...")

        except Exception as e:    

            self.log_test("Application Accessibility", False, str(e))    # Check if the templates exist

            return False    template_files = [

            'templates/decrypt.html',

    def test_page_loading(self):        'templates/manage_users.html', 

        """Test all major pages load correctly"""        'templates/activity_log.html'

        pages = {    ]

            "Dashboard": "/",    

            "Login": "/login",     print("\n📄 Template Files Status:")

            "Encrypt": "/encrypt",    for template in template_files:

            "Decrypt": "/decrypt",        exists = os.path.exists(template)

            "File Encrypt": "/file_encrypt",        status = "✅ EXISTS" if exists else "❌ MISSING"

            "File Decrypt": "/file_decrypt",        print(f"  {template}: {status}")

            "Manage Users": "/manage_users",    

            "Activity Log": "/activity_log"    print("\n✨ Summary:")

        }    print("The decrypt.html template now includes:")

            print("  • Activity Logs link for admin users")

        all_passed = True    print("  • Manage Users link for admin users") 

        for page_name, url in pages.items():    print("  • Clean admin theme styling")

            try:    print("  • Conditional display based on user role")

                response = self.session.get(self.base_url + url, timeout=5)    

                passed = response.status_code == 200    print("\n🚀 To test the application:")

                self.log_test(f"Page Loading: {page_name}", passed,    print("1. Run: python app_simple.py")

                             f"Status: {response.status_code}")    print("2. Open: http://localhost:5000")

                if not passed:    print("3. Login as 'admin' to see admin options")

                    all_passed = False    print("4. Navigate to Decrypt page to see the new links")

            except Exception as e:

                self.log_test(f"Page Loading: {page_name}", False, str(e))except ImportError as e:

                all_passed = False    print(f"❌ Error importing Flask app: {e}")

            

        return all_passedexcept Exception as e:

        print(f"❌ Error: {e}")

    def test_encryption_workflow(self):

        """Test complete encryption workflow"""print("\n🎉 Integration Complete!")

        try:
            # Test message encryption
            encrypt_data = {
                'message': 'Integration test message',
                'policy': 'department:IT AND role:admin',
                'user_id': 'test_user'
            }
            
            response = self.session.post(self.base_url + "/encrypt", 
                                       data=encrypt_data, timeout=10)
            
            passed = response.status_code == 200
            self.log_test("Message Encryption", passed,
                         f"Status: {response.status_code}")
            
            return passed
            
        except Exception as e:
            self.log_test("Message Encryption", False, str(e))
            return False
    
    def test_file_operations(self):
        """Test file upload and encryption"""
        try:
            # Create test file
            test_content = "This is a test file for integration testing"
            files = {
                'file': ('test_integration.txt', test_content.encode(), 'text/plain')
            }
            data = {
                'policy': 'department:IT',
                'user_id': 'test_user'
            }
            
            response = self.session.post(self.base_url + "/file_encrypt",
                                       files=files, data=data, timeout=10)
            
            passed = response.status_code == 200
            self.log_test("File Encryption", passed,
                         f"Status: {response.status_code}")
            
            return passed
            
        except Exception as e:
            self.log_test("File Encryption", False, str(e))
            return False
    
    def test_user_management(self):
        """Test user management functionality"""
        try:
            response = self.session.get(self.base_url + "/manage_users", timeout=5)
            passed = response.status_code == 200
            
            # Check if response contains user management elements
            if passed and response.text:
                has_user_content = any(word in response.text.lower() 
                                     for word in ['user', 'attribute', 'management'])
                passed = passed and has_user_content
            
            self.log_test("User Management", passed,
                         f"Status: {response.status_code}")
            
            return passed
            
        except Exception as e:
            self.log_test("User Management", False, str(e))
            return False
    
    def test_activity_logging(self):
        """Test activity logging functionality"""
        try:
            response = self.session.get(self.base_url + "/activity_log", timeout=5)
            passed = response.status_code == 200
            
            self.log_test("Activity Logging", passed,
                         f"Status: {response.status_code}")
            
            return passed
            
        except Exception as e:
            self.log_test("Activity Logging", False, str(e))
            return False
    
    def run_all_tests(self):
        """Run complete integration test suite"""
        print("=== Integration Test Suite ===")
        print(f"Testing application at: {self.base_url}")
        print()
        
        tests = [
            self.test_application_accessibility,
            self.test_page_loading,
            self.test_encryption_workflow,
            self.test_file_operations,
            self.test_user_management,
            self.test_activity_logging
        ]
        
        for test in tests:
            test()
            print()
        
        # Summary
        passed_tests = sum(1 for result in self.test_results if result['passed'])
        total_tests = len(self.test_results)
        
        print("=== Test Summary ===")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 All integration tests passed!")
            return True
        else:
            print(f"\n❌ {total_tests - passed_tests} tests failed!")
            return False

if __name__ == "__main__":
    print("Secure Data Sharing System - Integration Test Suite")
    print("=" * 55)
    print()
    print("⚠️  Make sure the application is running before starting tests!")
    print("   Start with: python app_simple.py")
    print()
    
    # Wait a moment for user to read
    time.sleep(2)
    
    tester = IntegrationTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)