<script lang="ts">
  import { onMount } from 'svelte';
  import { runAllTests } from '$lib/utils/apiTest';
  import { authStore } from '$lib/store/authStore';
  import { get } from 'svelte/store';

  let testResults = $state({
    achievements: null,
    plans: null
  });
  
  let isRunningTests = $state(false);
  let isAuthenticated = $state(false);

  onMount(() => {
    const auth = get(authStore);
    isAuthenticated = !!auth.accessToken;
  });

  async function handleRunTests() {
    if (!isAuthenticated) {
      alert('You must be logged in to run the tests');
      return;
    }
    
    isRunningTests = true;
    try {
      const results = await runAllTests();
      testResults = results;
    } catch (error) {
      console.error('Error running tests:', error);
    } finally {
      isRunningTests = false;
    }
  }
</script>

<div class="container mx-auto p-4 max-w-3xl">
  <h1 class="text-2xl font-bold mb-4">API Connectivity Test</h1>
  
  {#if !isAuthenticated}
    <div class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4" role="alert">
      <p class="font-bold">Warning</p>
      <p>You must be logged in to run the API tests. Please <a href="/login" class="underline">login</a> first.</p>
    </div>
  {:else}
    <button 
      on:click={handleRunTests}
      disabled={isRunningTests}
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-6 disabled:opacity-50"
    >
      {isRunningTests ? 'Running Tests...' : 'Run API Tests'}
    </button>
    
    {#if isRunningTests}
      <div class="flex justify-center items-center my-8">
        <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    {:else if testResults.achievements || testResults.plans}
      <div class="space-y-6">
        <!-- Achievements Test Results -->
        <div class="border rounded-lg overflow-hidden">
          <div class="bg-gray-100 px-4 py-2 border-b">
            <h2 class="text-lg font-semibold">Achievements Endpoint Test</h2>
          </div>
          <div class="p-4">
            {#if testResults.achievements}
              <div class={`p-3 rounded ${testResults.achievements.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                <p class="font-bold">{testResults.achievements.success ? 'Success' : 'Failed'}</p>
                <p>{testResults.achievements.message}</p>
              </div>
              
              {#if testResults.achievements.success && testResults.achievements.data}
                <div class="mt-4">
                  <h3 class="font-medium mb-2">Data Preview:</h3>
                  <pre class="bg-gray-50 p-3 rounded text-xs overflow-auto max-h-40">{JSON.stringify(testResults.achievements.data, null, 2)}</pre>
                </div>
              {/if}
            {/if}
          </div>
        </div>
        
        <!-- Plans Test Results -->
        <div class="border rounded-lg overflow-hidden">
          <div class="bg-gray-100 px-4 py-2 border-b">
            <h2 class="text-lg font-semibold">Plans Endpoint Test</h2>
          </div>
          <div class="p-4">
            {#if testResults.plans}
              <div class={`p-3 rounded ${testResults.plans.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                <p class="font-bold">{testResults.plans.success ? 'Success' : 'Failed'}</p>
                <p>{testResults.plans.message}</p>
              </div>
              
              {#if testResults.plans.success && testResults.plans.data}
                <div class="mt-4">
                  <h3 class="font-medium mb-2">Data Preview:</h3>
                  <pre class="bg-gray-50 p-3 rounded text-xs overflow-auto max-h-40">{JSON.stringify(testResults.plans.data, null, 2)}</pre>
                </div>
              {/if}
            {/if}
          </div>
        </div>
      </div>
    {/if}
  {/if}
  
  <div class="mt-8 text-sm text-gray-600">
    <h3 class="font-medium mb-2">Troubleshooting Tips:</h3>
    <ul class="list-disc pl-5 space-y-1">
      <li>Make sure the backend server is running on port 5000</li>
      <li>Check that you're logged in with valid credentials</li>
      <li>Verify that CORS is properly configured on the backend</li>
      <li>Check the browser console for detailed error messages</li>
    </ul>
  </div>
</div>
