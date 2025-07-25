#!/usr/bin/env python3
"""
Advanced Spintly API Tester with AWS Cognito Authentication
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

class SpintlyAdvancedTester:
    def __init__(self, investigation_file: str):
        with open(investigation_file, 'r') as f:
            self.data = json.load(f)

        self.session = requests.Session()

        # Extract authentication data
        auth_data = self.data.get('authData', {})
        local_storage = auth_data.get('localStorage', {})

        # Get AWS Cognito tokens
        self.access_token = local_storage.get('CognitoIdentityServiceProvider.24lqc87njds5aqjknibohr5ero.+918086516291.accessToken', '')
        self.id_token = local_storage.get('CognitoIdentityServiceProvider.24lqc87njds5aqjknibohr5ero.+918086516291.idToken', '')
        self.base_url = local_storage.get('baseURL', 'https://saams.api.spintly.com')
        self.user_id = '97b34de5-1854-4006-90ae-b0d2a140bb8d'  # From investigation

        # Setup headers
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': auth_data.get('userAgent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            'Origin': 'https://smart-access.spintly.com',
            'Referer': 'https://smart-access.spintly.com/dashboard/access/history'
        }

        print(f"🔑 Using Base URL: {self.base_url}")
        print(f"🎫 Access Token: {self.access_token[:50]}...")
        print(f"👤 User ID: {self.user_id}")

    def test_endpoint(self, url: str, method: str = 'GET', data: dict = None, description: str = "") -> Dict:
        """Test an API endpoint with proper authentication"""
        print(f"\n🧪 Testing: {method} {url}")
        print(f"📝 Description: {description}")

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                timeout=30
            )

            print(f"📊 Status: {response.status_code}")
            print(f"📏 Content Length: {len(response.content)}")

            result = {
                'url': url,
                'method': method,
                'status_code': response.status_code,
                'success': 200 <= response.status_code < 300,
                'headers': dict(response.headers),
                'content_type': response.headers.get('content-type', ''),
                'content_length': len(response.content),
                'timestamp': datetime.now().isoformat()
            }

            # Try to parse response
            try:
                json_response = response.json()
                result['json_response'] = json_response
                print(f"✅ JSON Response received with {len(json_response) if isinstance(json_response, list) else 'object'} items")

                # If it's access history data, show sample
                if isinstance(json_response, list) and len(json_response) > 0:
                    print(f"📋 Sample data: {json_response[0] if json_response else 'Empty'}")

            except:
                result['text_response'] = response.text[:500]
                if response.status_code == 200:
                    print(f"📄 Text response: {response.text[:100]}...")
                else:
                    print(f"❌ Error response: {response.text[:200]}")

            return result

        except Exception as e:
            print(f"💥 Exception: {str(e)}")
            return {
                'url': url,
                'method': method,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }

    def test_spintly_api_endpoints(self) -> List[Dict]:
        """Test various Spintly API endpoint patterns"""
        print("🎯 TESTING SPINTLY API ENDPOINTS WITH AUTHENTICATION")
        print("=" * 60)

        endpoints_to_test = [
            # Direct API endpoints
            (f"{self.base_url}/access/history", "GET", "Access history from API base"),
            (f"{self.base_url}/access/logs", "GET", "Access logs from API base"),
            (f"{self.base_url}/user/access-history", "GET", "User access history"),
            (f"{self.base_url}/dashboard/access/history", "GET", "Dashboard access history"),
            (f"{self.base_url}/api/access/history", "GET", "API access history"),
            (f"{self.base_url}/api/v1/access/history", "GET", "API v1 access history"),
            (f"{self.base_url}/api/v2/access/history", "GET", "API v2 access history"),

            # User-specific endpoints
            (f"{self.base_url}/users/{self.user_id}/access", "GET", "User-specific access"),
            (f"{self.base_url}/users/{self.user_id}/history", "GET", "User-specific history"),
            (f"{self.base_url}/api/users/{self.user_id}/access", "GET", "API user access"),

            # Organization endpoints (ARAMIS from data)
            (f"{self.base_url}/organizations/access/history", "GET", "Organization access history"),
            (f"{self.base_url}/api/organizations/access", "GET", "API organization access"),

            # Common patterns
            (f"{self.base_url}/events", "GET", "Events endpoint"),
            (f"{self.base_url}/api/events", "GET", "API events endpoint"),
            (f"{self.base_url}/logs", "GET", "Logs endpoint"),
            (f"{self.base_url}/api/logs", "GET", "API logs endpoint"),
        ]

        results = []
        for url, method, description in endpoints_to_test:
            result = self.test_endpoint(url, method, description=description)
            results.append(result)
            time.sleep(0.5)  # Rate limiting

        return results

    def test_with_different_auth_headers(self) -> List[Dict]:
        """Test with different authentication header formats"""
        print("\n🔐 TESTING DIFFERENT AUTHENTICATION METHODS")
        print("=" * 50)

        # Test different auth header formats
        auth_variations = [
            {'Authorization': f'Bearer {self.access_token}'},
            {'Authorization': f'JWT {self.access_token}'},
            {'Authorization': f'Token {self.access_token}'},
            {'X-Auth-Token': self.access_token},
            {'X-Access-Token': self.access_token},
            {'Authorization': f'Bearer {self.id_token}'},  # Try ID token instead
        ]

        test_url = f"{self.base_url}/access/history"
        results = []

        for i, auth_header in enumerate(auth_variations):
            print(f"\n🔑 Auth Method {i+1}: {list(auth_header.keys())[0]}")

            # Create temporary headers
            temp_headers = self.headers.copy()
            temp_headers.update(auth_header)

            try:
                response = self.session.get(test_url, headers=temp_headers, timeout=30)

                result = {
                    'auth_method': list(auth_header.keys())[0],
                    'status_code': response.status_code,
                    'success': 200 <= response.status_code < 300,
                    'content_length': len(response.content)
                }

                print(f"📊 Status: {response.status_code}")

                if response.status_code == 200:
                    try:
                        json_data = response.json()
                        result['has_data'] = len(json_data) > 0 if isinstance(json_data, list) else True
                        print(f"✅ SUCCESS! Got data: {len(json_data) if isinstance(json_data, list) else 'object'}")
                    except:
                        result['has_data'] = False
                        print(f"✅ SUCCESS! Got text response")

                results.append(result)

            except Exception as e:
                print(f"❌ Error: {str(e)}")
                results.append({
                    'auth_method': list(auth_header.keys())[0],
                    'error': str(e),
                    'success': False
                })

            time.sleep(0.5)

        return results

    def generate_working_curl_commands(self, successful_results: List[Dict]) -> List[str]:
        """Generate curl commands for successful endpoints"""
        print("\n🔧 GENERATING WORKING CURL COMMANDS")
        print("=" * 40)

        curl_commands = []

        for result in successful_results:
            if result.get('success'):
                url = result['url']

                curl = f'curl -X {result["method"]} "{url}"'
                curl += f' \\\n  -H "Authorization: Bearer {self.access_token}"'
                curl += f' \\\n  -H "Content-Type: application/json"'
                curl += f' \\\n  -H "Accept: application/json"'
                curl += f' \\\n  -H "User-Agent: {self.headers["User-Agent"]}"'
                curl += f' \\\n  -H "Origin: https://smart-access.spintly.com"'
                curl += f' \\\n  -H "Referer: https://smart-access.spintly.com/dashboard/access/history"'

                curl_commands.append(curl)

                print(f"\n✅ Working endpoint: {url}")
                print(curl)

        return curl_commands

    def save_results(self, all_results: List[Dict], auth_results: List[Dict]):
        """Save all test results"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'authentication': {
                'base_url': self.base_url,
                'user_id': self.user_id,
                'access_token_preview': self.access_token[:50] + '...',
                'id_token_preview': self.id_token[:50] + '...'
            },
            'endpoint_tests': all_results,
            'auth_method_tests': auth_results,
            'successful_endpoints': [r for r in all_results if r.get('success')],
            'summary': {
                'total_endpoint_tests': len(all_results),
                'successful_endpoint_tests': len([r for r in all_results if r.get('success')]),
                'total_auth_tests': len(auth_results),
                'successful_auth_tests': len([r for r in auth_results if r.get('success')])
            }
        }

        with open('advanced_api_test_results.json', 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n💾 Results saved to: advanced_api_test_results.json")
        return output

def main():
    tester = SpintlyAdvancedTester('spintly_investigation_results.json')

    # Test API endpoints
    endpoint_results = tester.test_spintly_api_endpoints()

    # Test different auth methods
    auth_results = tester.test_with_different_auth_headers()

    # Generate curl commands for successful tests
    successful_endpoints = [r for r in endpoint_results if r.get('success')]
    if successful_endpoints:
        curl_commands = tester.generate_working_curl_commands(successful_endpoints)

    # Save results
    output = tester.save_results(endpoint_results, auth_results)

    print(f"\n📊 FINAL SUMMARY")
    print("=" * 30)
    print(f"Endpoint tests: {output['summary']['successful_endpoint_tests']}/{output['summary']['total_endpoint_tests']} successful")
    print(f"Auth method tests: {output['summary']['successful_auth_tests']}/{output['summary']['total_auth_tests']} successful")

    if output['summary']['successful_endpoint_tests'] > 0:
        print(f"\n🎉 Found {output['summary']['successful_endpoint_tests']} working API endpoints!")
        print("Ready to build the FastAPI wrapper!")
    else:
        print(f"\n🤔 No working endpoints found. The API might use:")
        print("- Different authentication method")
        print("- Server-side rendering only")
        print("- Different base URL")
        print("- Additional headers or parameters")

if __name__ == "__main__":
    main()