#!/usr/bin/env python3
"""
Spintly API Tester
Test discovered API endpoints and validate authentication
"""

import requests
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class APIEndpoint:
    url: str
    method: str
    headers: Dict[str, str]
    cookies: Dict[str, str]
    body: Optional[str] = None
    description: str = ""

class SpintlyAPITester:
    def __init__(self, investigation_results_file: str):
        """Initialize with investigation results"""
        with open(investigation_results_file, 'r') as f:
            self.data = json.load(f)

        self.session = requests.Session()
        self.base_headers = {
            'User-Agent': self.data.get('authData', {}).get('userAgent',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        # Set cookies from investigation
        cookies = self.data.get('authData', {}).get('cookies', {})
        for name, value in cookies.items():
            self.session.cookies.set(name, value)

    def test_endpoint(self, endpoint: APIEndpoint) -> Dict:
        """Test a single API endpoint"""
        print(f"\n🧪 Testing: {endpoint.method} {endpoint.url}")
        print(f"📝 Description: {endpoint.description}")

        headers = {**self.base_headers, **endpoint.headers}

        try:
            response = self.session.request(
                method=endpoint.method,
                url=endpoint.url,
                headers=headers,
                data=endpoint.body,
                timeout=30
            )

            result = {
                'url': endpoint.url,
                'method': endpoint.method,
                'status_code': response.status_code,
                'success': 200 <= response.status_code < 300,
                'headers': dict(response.headers),
                'content_type': response.headers.get('content-type', ''),
                'content_length': len(response.content),
                'timestamp': datetime.now().isoformat()
            }

            # Try to parse JSON response
            try:
                result['json_response'] = response.json()
                print(f"✅ Success: {response.status_code} - JSON response received")
            except:
                result['text_response'] = response.text[:500]  # First 500 chars
                print(f"📄 Success: {response.status_code} - Text response received")

            return result

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                'url': endpoint.url,
                'method': endpoint.method,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }

    def test_discovered_endpoints(self) -> List[Dict]:
        """Test all discovered API endpoints"""
        print("🔍 TESTING DISCOVERED API ENDPOINTS")
        print("=" * 50)

        results = []
        api_requests = self.data.get('findings', {}).get('apiRequests', [])

        if not api_requests:
            print("⚠️ No API requests found in investigation results")
            return results

        for i, req in enumerate(api_requests):
            endpoint = APIEndpoint(
                url=req.get('url', ''),
                method=req.get('method', 'GET'),
                headers=req.get('headers', {}),
                cookies=req.get('cookies', {}),
                body=req.get('body'),
                description=f"Discovered endpoint {i+1}"
            )

            result = self.test_endpoint(endpoint)
            results.append(result)

            # Rate limiting - wait between requests
            time.sleep(1)

        return results

    def test_common_endpoints(self) -> List[Dict]:
        """Test common API endpoint patterns"""
        print("\n🎯 TESTING COMMON ENDPOINT PATTERNS")
        print("=" * 50)

        base_url = "https://smart-access.spintly.com"
        common_endpoints = [
            APIEndpoint(f"{base_url}/api/access/history", "GET", {}, {}, description="Access history API"),
            APIEndpoint(f"{base_url}/api/access/logs", "GET", {}, {}, description="Access logs API"),
            APIEndpoint(f"{base_url}/api/dashboard/access", "GET", {}, {}, description="Dashboard access API"),
            APIEndpoint(f"{base_url}/dashboard/access/history", "GET", {}, {}, description="Dashboard page"),
            APIEndpoint(f"{base_url}/api/user/access-history", "GET", {}, {}, description="User access history"),
        ]

        results = []
        for endpoint in common_endpoints:
            result = self.test_endpoint(endpoint)
            results.append(result)
            time.sleep(1)

        return results

    def generate_curl_commands(self, results: List[Dict]) -> List[str]:
        """Generate curl commands for successful endpoints"""
        print("\n🔧 GENERATING CURL COMMANDS")
        print("=" * 50)

        curl_commands = []

        for result in results:
            if result.get('success'):
                cookies = '; '.join([f"{k}={v}" for k, v in self.session.cookies.items()])

                curl = f"curl -X {result['method']} \"{result['url']}\""
                curl += f" \\\n  -H \"User-Agent: {self.base_headers['User-Agent']}\""
                curl += f" \\\n  -H \"Accept: {self.base_headers['Accept']}\""

                if cookies:
                    curl += f" \\\n  -H \"Cookie: {cookies}\""

                curl_commands.append(curl)
                print(f"\n✅ {result['url']}")
                print(curl)

        return curl_commands

    def save_results(self, results: List[Dict], filename: str = "api_test_results.json"):
        """Save test results to file"""
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(results),
            'successful_tests': len([r for r in results if r.get('success')]),
            'failed_tests': len([r for r in results if not r.get('success')]),
            'results': results
        }

        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"\n💾 Results saved to: {filename}")
        return output

def main():
    """Main testing function"""
    import sys

    if len(sys.argv) != 2:
        print("Usage: python api_tester.py <investigation_results.json>")
        sys.exit(1)

    results_file = sys.argv[1]

    try:
        tester = SpintlyAPITester(results_file)

        # Test discovered endpoints
        discovered_results = tester.test_discovered_endpoints()

        # Test common patterns
        common_results = tester.test_common_endpoints()

        # Combine results
        all_results = discovered_results + common_results

        # Generate curl commands
        curl_commands = tester.generate_curl_commands(all_results)

        # Save results
        output = tester.save_results(all_results)

        print(f"\n📊 SUMMARY")
        print("=" * 20)
        print(f"Total tests: {output['total_tests']}")
        print(f"Successful: {output['successful_tests']}")
        print(f"Failed: {output['failed_tests']}")

        if curl_commands:
            print(f"\n🎉 Found {len(curl_commands)} working endpoints!")
            print("Check api_test_results.json for details")
        else:
            print("\n⚠️ No working endpoints found. Check authentication.")

    except FileNotFoundError:
        print(f"❌ Investigation results file not found: {results_file}")
        print("Please run the browser investigation first.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()