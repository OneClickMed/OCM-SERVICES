#!/bin/bash

# API Testing Script for OCM Email Service
# Token: 00ded67f93cf58d48e6ae111f2be119d9e7ca243
# Email: nelsonfai21@yahoo.com
# Environment: test

BASE_URL="http://localhost:8000/api"
TOKEN="00ded67f93cf58d48e6ae111f2be119d9e7ca243"
EMAIL="nelsonfai21@yahoo.com"
ENVIRONMENT="test"

echo "================================================"
echo "OCM Email Service - API Endpoint Tests"
echo "================================================"
echo ""

# Test 1: Health Check (No Auth Required)
echo "1. Testing Health Check Endpoint"
echo "GET ${BASE_URL}/health/"
echo "---"
curl -X GET "${BASE_URL}/health/" \
  -H "Content-Type: application/json" \
  -w "\n\nHTTP Status: %{http_code}\n" \
  -s
echo ""
echo "================================================"
echo ""

# Test 2: Email Verification (Updated with Product Branding)
echo "2. Testing Email Verification Endpoint (with product branding)"
echo "POST ${BASE_URL}/email/verification/"
echo "---"
curl -X POST "${BASE_URL}/email/verification/" \
  -H "Authorization: Token ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"${EMAIL}\",
    \"user_name\": \"Nelson Fai\",
    \"environment\": \"${ENVIRONMENT}\"
  }" \
  -w "\n\nHTTP Status: %{http_code}\n" \
  -s
echo ""
echo "================================================"
echo ""

# Test 3: Welcome Email (New Endpoint)
echo "3. Testing Welcome Email Endpoint (NEW)"
echo "POST ${BASE_URL}/email/welcome/"
echo "---"
curl -X POST "${BASE_URL}/email/welcome/" \
  -H "Authorization: Token ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"${EMAIL}\",
    \"user_name\": \"Nelson Fai\",
    \"environment\": \"${ENVIRONMENT}\"
  }" \
  -w "\n\nHTTP Status: %{http_code}\n" \
  -s
echo ""
echo "================================================"
echo ""

# Test 4: Generic Email
echo "4. Testing Generic Email Endpoint"
echo "POST ${BASE_URL}/email/generic/"
echo "---"
curl -X POST "${BASE_URL}/email/generic/" \
  -H "Authorization: Token ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"to_email\": \"${EMAIL}\",
    \"subject\": \"Test Email from OCM Service\",
    \"html_content\": \"<h1>Hello Nelson!</h1><p>This is a test email from OCM Service in test mode.</p>\",
    \"text_content\": \"Hello Nelson! This is a test email from OCM Service in test mode.\",
    \"environment\": \"${ENVIRONMENT}\"
  }" \
  -w "\n\nHTTP Status: %{http_code}\n" \
  -s
echo ""
echo "================================================"
echo ""

# Test 5: Verification Confirmation Page (No Auth Required)
echo "5. Testing Verification Confirmation Page (GET request)"
echo "GET ${BASE_URL}/email/verify-confirmation/?token=test-token&environment=test&product=Test%20Product"
echo "---"
echo "Note: This returns HTML, so we'll just check the status code"
curl -X GET "${BASE_URL}/email/verify-confirmation/?token=test-token&environment=${ENVIRONMENT}&product=Test%20Product" \
  -w "\nHTTP Status: %{http_code}\n" \
  -s -o /dev/null
echo ""
echo "================================================"
echo ""

# Test 6: Password Reset
echo "6. Testing Password Reset Endpoint"
echo "POST ${BASE_URL}/email/password-reset/"
echo "---"
curl -X POST "${BASE_URL}/email/password-reset/" \
  -H "Authorization: Token ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"${EMAIL}\",
    \"user_name\": \"Nelson Fai\",
    \"environment\": \"${ENVIRONMENT}\"
  }" \
  -w "\n\nHTTP Status: %{http_code}\n" \
  -s
echo ""
echo "================================================"
echo ""

# Test 7: Forgot Password
echo "7. Testing Forgot Password Endpoint"
echo "POST ${BASE_URL}/email/forgot-password/"
echo "---"
curl -X POST "${BASE_URL}/email/forgot-password/" \
  -H "Authorization: Token ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"${EMAIL}\",
    \"user_name\": \"Nelson Fai\",
    \"environment\": \"${ENVIRONMENT}\"
  }" \
  -w "\n\nHTTP Status: %{http_code}\n" \
  -s
echo ""
echo "================================================"
echo ""

echo "Testing Complete!"
echo ""
echo "Summary:"
echo "- Token Used: ${TOKEN}"
echo "- Test Email: ${EMAIL}"
echo "- Environment: ${ENVIRONMENT}"
echo ""
echo "Check your email (${EMAIL}) for the test messages!"
