#!/usr/bin/env python3
"""
Spintly Endpoint Discovery - Try to find the actual API endpoints
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List

class SpintlyEndpointDiscovery:
    def __init__(self, investigation_file: str):
        with open(investigation_file, 'r') as f:
            self.data = json.load(f)

        self.session = requests.Session()

        # Extract authentication data
        auth_data = self.data.get('authData', {})
        local_storage = auth_data.get('localStorage', {})

        self.access_token = local_storage.get('CognitoIdentityServiceProvider.24lqc87njds5aqjknibohr5ero.+918086516291.accessToken', '')
        self.base_url = local_storage.get('baseURL', 'https://saams.api.spintly.com')
        self.user_id = '97b34de5-1854-4006-90ae-b0d2a140bb8d'

        # Setup headers
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': auth_data.get('userAgent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            'Origin': 'https://smart-access.spintly.com',
            'Referer': 'https://smart-access.spintly.com/dashboard/access/history'
        }

        print(f"🔍 ENDPOINT DISCOVERY MODE")
        print(f"🔑 Base URL: {self.base_url}")
        print(f"👤 User ID: {self.user_id}")

    def test_graphql_endpoints(self):
        """Test if Spintly uses GraphQL"""
        print("\n🔍 TESTING GRAPHQL ENDPOINTS")
        print("=" * 40)

        graphql_endpoints = [
            f"{self.base_url}/graphql",
            f"{self.base_url}/api/graphql",
            "https://smart-access.spintly.com/graphql",
            "https://smart-access.spintly.com/api/graphql"
        ]

        # Common GraphQL query for access history
        graphql_query = {
            "query": """
            query GetAccessHistory {
                accessHistory {
                    id
                    user
                    timestamp
                    direction
                    location
                }
            }
            """
        }

        for endpoint in graphql_endpoints:
            print(f"\n🧪 Testing GraphQL: {endpoint}")
            try:
                response = self.session.post(endpoint, headers=self.headers, json=graphql_query, timeout=30)
                print(f"📊 Status: {response.status_code}")

                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"✅ GraphQL SUCCESS! Response: {data}")
                        return endpoint, data
                    except:
                        print(f"📄 Text response: {response.text[:200]}")
                elif response.status_code != 404:
                    print(f"🤔 Interesting response: {response.text[:200]}")

            except Exception as e:
                print(f"❌ Error: {str(e)}")

            time.sleep(0.5)

        return None, None