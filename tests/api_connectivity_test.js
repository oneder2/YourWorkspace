/**
 * API Connectivity Test Script
 * 
 * This script tests the connectivity to the backend API endpoints
 * for achievements and plans to ensure they are working correctly.
 * 
 * Usage:
 * 1. Make sure the backend server is running on port 5000
 * 2. Run this script with Node.js: node api_connectivity_test.js
 */

const fetch = require('node-fetch');

// Configuration
const API_BASE_URL = 'http://localhost:5000/api/v1';
const TEST_CREDENTIALS = {
  email: 'test@example.com',
  password: 'password123'
};

// Test endpoints
const ENDPOINTS = {
  login: '/auth/login',
  achievements: '/achievements',
  plans: '/plans'
};

// Helper function to log results
function logResult(endpoint, success, message) {
  const status = success ? '✅ PASS' : '❌ FAIL';
  console.log(`${status} - ${endpoint}: ${message}`);
}

// Main test function
async function runTests() {
  console.log('🔍 Starting API Connectivity Tests...');
  console.log('======================================');
  
  let accessToken = null;
  
  // Test 1: Login to get access token
  try {
    console.log('🔑 Testing authentication...');
    const loginResponse = await fetch(`${API_BASE_URL}${ENDPOINTS.login}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(TEST_CREDENTIALS)
    });
    
    const loginData = await loginResponse.json();
    
    if (loginResponse.ok && loginData.access_token) {
      accessToken = loginData.access_token;
      logResult(ENDPOINTS.login, true, 'Successfully authenticated');
    } else {
      logResult(ENDPOINTS.login, false, `Authentication failed: ${loginData.message || 'Unknown error'}`);
      console.log('⚠️ Cannot proceed with further tests without authentication');
      return;
    }
  } catch (error) {
    logResult(ENDPOINTS.login, false, `Error: ${error.message}`);
    console.log('⚠️ Cannot proceed with further tests without authentication');
    return;
  }
  
  // Test 2: Get achievements
  try {
    console.log('\n🏆 Testing achievements endpoint...');
    const achievementsResponse = await fetch(`${API_BASE_URL}${ENDPOINTS.achievements}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    
    if (achievementsResponse.ok) {
      const achievementsData = await achievementsResponse.json();
      logResult(ENDPOINTS.achievements, true, `Successfully retrieved ${achievementsData.length} achievements`);
    } else {
      const errorData = await achievementsResponse.text();
      logResult(ENDPOINTS.achievements, false, `Failed with status ${achievementsResponse.status}: ${errorData}`);
    }
  } catch (error) {
    logResult(ENDPOINTS.achievements, false, `Error: ${error.message}`);
  }
  
  // Test 3: Get plans
  try {
    console.log('\n📝 Testing plans endpoint...');
    const plansResponse = await fetch(`${API_BASE_URL}${ENDPOINTS.plans}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`
      }
    });
    
    if (plansResponse.ok) {
      const plansData = await plansResponse.json();
      logResult(ENDPOINTS.plans, true, `Successfully retrieved ${plansData.length} plans`);
    } else {
      const errorData = await plansResponse.text();
      logResult(ENDPOINTS.plans, false, `Failed with status ${plansResponse.status}: ${errorData}`);
    }
  } catch (error) {
    logResult(ENDPOINTS.plans, false, `Error: ${error.message}`);
  }
  
  console.log('\n======================================');
  console.log('🏁 API Connectivity Tests Completed');
}

// Run the tests
runTests().catch(error => {
  console.error('❌ Test execution failed:', error);
});
