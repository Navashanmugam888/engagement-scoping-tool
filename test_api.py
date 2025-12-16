"""
Quick test script to verify Python API is working
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    print("\n" + "="*60)
    print("Testing Health Check Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_roles():
    """Test roles endpoint"""
    print("\n" + "="*60)
    print("Testing Roles Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/roles")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Available Roles: {len(data.get('roles', []))}")
        print(f"Roles: {', '.join(data.get('roles', [])[:3])}...")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_submit():
    """Test scoping submission"""
    print("\n" + "="*60)
    print("Testing Scoping Submission")
    print("="*60)
    
    # Sample payload
    payload = {
        "userEmail": "test@example.com",
        "userName": "Test User",
        "scopingData": {
            "dimensions-account": {"value": "YES", "count": 0},
            "dimensions-multiCurrency": {"value": "YES", "count": 5},
            "dimensions-reportingCurrency": {"value": "YES", "count": 2},
            "dimensions-entity": {"value": "YES", "count": 3},
            "features-consolidationJournals": {"value": "YES", "count": 0},
            "features-cashFlow": {"value": "YES", "count": 0}
        },
        "selectedRoles": ["PM USA", "PM India", "Architect USA"],
        "comments": "Test submission from test script",
        "submittedAt": "2025-12-04T14:30:00Z"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/scoping/submit",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"Submission ID: {data.get('submission_id')}")
            print(f"Tier: {data.get('result', {}).get('tier')}")
            print(f"Total Hours: {data.get('result', {}).get('total_hours')}")
            print(f"Total Days: {data.get('result', {}).get('total_days')}")
            return data.get('submission_id')
        else:
            print(f"❌ Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_history(email="test@example.com"):
    """Test history endpoint"""
    print("\n" + "="*60)
    print("Testing History Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/scoping/history?email={email}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            submissions = data.get('submissions', [])
            print(f"✅ Found {len(submissions)} submission(s)")
            
            if submissions:
                latest = submissions[0]
                print(f"\nLatest Submission:")
                print(f"  ID: {latest.get('id')}")
                print(f"  Date: {latest.get('submitted_at')}")
                print(f"  Status: {latest.get('status')}")
            
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  PYTHON API TEST SUITE")
    print("="*60)
    print(f"\nBase URL: {BASE_URL}")
    print("\nMake sure the Python API is running:")
    print("  python engagement-scoping-tool/api_server.py")
    print("")
    
    input("Press Enter to start tests...")
    
    # Run tests
    results = []
    
    results.append(("Health Check", test_health()))
    results.append(("Roles Endpoint", test_roles()))
    
    submission_id = test_submit()
    results.append(("Submission", submission_id is not None))
    
    if submission_id:
        results.append(("History", test_history()))
    
    # Summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print("")
    print(f"Total: {passed}/{total} tests passed")
    print("="*60)


if __name__ == "__main__":
    main()
