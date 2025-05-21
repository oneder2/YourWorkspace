/**
 * API Test Utility
 * 
 * This utility provides functions to test the API connectivity
 * from the frontend to the backend for achievements and plans.
 */

import { api } from '../services/api';

// Test endpoints
const ENDPOINTS = {
  achievements: '/achievements',
  plans: '/plans'
};

/**
 * Tests the connectivity to the achievements API endpoint.
 * @returns {Promise<{success: boolean, message: string, data?: any}>} Test result
 */
export async function testAchievementsEndpoint() {
  try {
    console.log('Testing achievements endpoint...');
    const response = await api.get(ENDPOINTS.achievements);
    
    return {
      success: true,
      message: `Successfully retrieved ${response.length} achievements`,
      data: response
    };
  } catch (error: any) {
    console.error('Error testing achievements endpoint:', error);
    return {
      success: false,
      message: `Error: ${error.message || 'Unknown error'}`
    };
  }
}

/**
 * Tests the connectivity to the plans API endpoint.
 * @returns {Promise<{success: boolean, message: string, data?: any}>} Test result
 */
export async function testPlansEndpoint() {
  try {
    console.log('Testing plans endpoint...');
    const response = await api.get(ENDPOINTS.plans);
    
    return {
      success: true,
      message: `Successfully retrieved ${response.length} plans`,
      data: response
    };
  } catch (error: any) {
    console.error('Error testing plans endpoint:', error);
    return {
      success: false,
      message: `Error: ${error.message || 'Unknown error'}`
    };
  }
}

/**
 * Runs all API tests and returns the results.
 * @returns {Promise<{achievements: {success: boolean, message: string, data?: any}, plans: {success: boolean, message: string, data?: any}}>} Test results
 */
export async function runAllTests() {
  const achievementsResult = await testAchievementsEndpoint();
  const plansResult = await testPlansEndpoint();
  
  return {
    achievements: achievementsResult,
    plans: plansResult
  };
}
