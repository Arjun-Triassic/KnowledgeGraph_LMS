#!/bin/bash

# Test script for KnowledgeGraph LMS API
# Make sure the server is running on http://127.0.0.1:8000

BASE_URL="http://127.0.0.1:8000"
ADMIN_USER_ID=1  # Change this to your bootstrap admin user ID

echo "=== Testing KnowledgeGraph LMS API ==="
echo ""

# 1. Create a new user
echo "1. Creating a new user..."
RESPONSE=$(curl -s -X 'POST' \
  "${BASE_URL}/users/" \
  -H "X-User-Id: ${ADMIN_USER_ID}" \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "role": "learner"
  }')

echo "Response: $RESPONSE"
echo ""

# 2. List all users
echo "2. Listing all users..."
curl -s -X 'GET' \
  "${BASE_URL}/users/" \
  -H "X-User-Id: ${ADMIN_USER_ID}" | jq '.'
echo ""

# 3. Get user by ID (assuming user ID 2 exists)
echo "3. Getting user by ID 2..."
curl -s -X 'GET' \
  "${BASE_URL}/users/2" \
  -H "X-User-Id: ${ADMIN_USER_ID}" | jq '.'
echo ""

echo "=== Test Complete ==="

