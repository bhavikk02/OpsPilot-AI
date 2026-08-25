import requests


BASE_URL = "http://127.0.0.1:8000"


# ============================================================
# Test 1: Health endpoint
# ============================================================

def test_health():

    response = requests.get(
        f"{BASE_URL}/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Application is Running"
    assert data["service"] == "OpsPilot AI"

    print("PASS: Health endpoint")


# ============================================================
# Test 2: Supported question
# ============================================================

def test_supported_question():

    response = requests.post(
        f"{BASE_URL}/ask",
        json={
            "question":
                "How do I troubleshoot a Kubernetes CrashLoopBackOff?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["relevant"] is True
    assert data["relevance_decision"] == "YES"
    assert data["answer"]
    assert "kubernetes.md" in data["sources"]

    print("PASS: Supported question")


# ============================================================
# Test 3: Unsupported question
# ============================================================

def test_unsupported_question():

    response = requests.post(
        f"{BASE_URL}/ask",
        json={
            "question":
                "How do I troubleshoot a Kubernetes Ingress 502 error?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["relevant"] is False
    assert data["relevance_decision"] == "NO"

    assert (
        "don't have enough relevant information"
        in data["answer"].lower()
    )

    print("PASS: Unsupported question")


# ============================================================
# Test 4: Empty question
# ============================================================

def test_empty_question():

    response = requests.post(
        f"{BASE_URL}/ask",
        json={
            "question": "   "
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert "Question cannot be empty." in str(data)

    print("PASS: Empty question validation")


# ============================================================
# Run all tests
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("OPSPILOT API E2E TEST")
    print("=" * 60)

    tests = [
        test_health,
        test_supported_question,
        test_unsupported_question,
        test_empty_question
    ]

    passed = 0

    for test in tests:

        try:

            test()

            passed += 1

        except Exception as error:

            print(
                f"FAIL: {test.__name__}"
            )

            print(
                f"Reason: {error}"
            )

    print("\n" + "=" * 60)
    print(
        f"RESULT: {passed}/{len(tests)} tests passed"
    )
    print("=" * 60)