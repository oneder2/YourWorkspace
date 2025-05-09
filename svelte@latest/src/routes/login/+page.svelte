<script lang="ts">
  import { goto } from '$app/navigation';
  import { authService, type LoginCredentials, type ApiError } from '$lib/services/authService';
  import { isAuthenticated } from '$lib/store/authStore';
  import { onMount } from 'svelte';

  let email = '';
  let password = '';
  let errorMessage = '';
  let isLoading = false;

  // If the user is already authenticated, redirect them away from the login page.
  onMount(() => {
    const unsubscribe = isAuthenticated.subscribe(authenticated => {
      if (authenticated) {
        goto('/doing'); // Or your default authenticated route
      }
    });
    return unsubscribe; // Cleanup subscription on component destroy
  });

  async function handleLogin() {
    isLoading = true;
    errorMessage = '';
    const credentials: LoginCredentials = { email, password };

    try {
      await authService.loginUser(credentials);
      // The authStore will be updated by loginUser,
      // and the onMount subscription to isAuthenticated should trigger redirection.
      // If not, or for immediate feedback:
      // await goto('/doing'); // Or your default authenticated route
    } catch (error: any) {
      const apiError = error as ApiError;
      if (apiError.data && apiError.data.message) {
        errorMessage = apiError.data.message;
      } else if (apiError.message) {
        errorMessage = apiError.message;
      } else {
        errorMessage = 'An unexpected error occurred. Please try again.';
      }
      console.error('Login page error:', apiError);
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="login-container">
  <div class="login-card">
    <h1 class="card-title">Login</h1>
    <p class="card-subtitle">Welcome back! Please enter your credentials.</p>

    <form on:submit|preventDefault={handleLogin} class="login-form">
      <div class="form-group">
        <label for="email">Email Address</label>
        <input
          type="email"
          id="email"
          bind:value={email}
          required
          placeholder="you@example.com"
          disabled={isLoading}
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          bind:value={password}
          required
          placeholder="••••••••"
          disabled={isLoading}
        />
      </div>

      {#if errorMessage}
        <div class="error-message">
          <p>{errorMessage}</p>
        </div>
      {/if}

      <button type="submit" class="submit-button" disabled={isLoading}>
        {#if isLoading}
          <span>Loading...</span>
        {:else}
          <span>Login</span>
        {/if}
      </button>
    </form>

    <div class="alternative-action">
      <p>
        Don't have an account?
        <a href="/register">Sign up here</a>
      </p>
    </div>
  </div>
</div>

<style>
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh; /* Adjust as needed, considering navbar etc. */
    padding: 2rem 1rem;
    background-color: var(--light-color, #f4f7f9); /* From global.css or default */
  }

  .login-card {
    background-color: #ffffff;
    padding: 2.5rem 2rem;
    border-radius: var(--border-radius, 0.375rem);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1), 0 5px 10px rgba(0, 0, 0, 0.04);
    width: 100%;
    max-width: 420px; /* Max width of the card */
  }

  .card-title {
    font-size: 2rem; /* Consistent with global.css h1 if possible */
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.5rem;
    color: var(--text-primary, #212529);
  }

  .card-subtitle {
    text-align: center;
    margin-bottom: 2rem;
    color: var(--text-secondary, #6c757d);
    font-size: 0.95rem;
  }

  .login-form .form-group {
    margin-bottom: 1.5rem;
  }

  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: var(--text-primary, #333);
  }

  .form-group input {
    width: 100%;
    padding: 0.75rem 1rem; /* Slightly larger padding for better touch targets */
    border: 1px solid #ced4da;
    border-radius: var(--border-radius, 0.375rem);
    font-size: 1rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  }

  .form-group input:focus {
    border-color: var(--primary-color, #007bff);
    box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    outline: none;
  }

   .form-group input:disabled {
    background-color: #e9ecef;
    opacity: 0.7;
  }

  .error-message {
    background-color: rgba(220, 53, 69, 0.1); /* --danger-color with opacity */
    color: var(--danger-color, #dc3545);
    padding: 0.75rem 1rem;
    border-radius: var(--border-radius, 0.375rem);
    margin-bottom: 1.5rem;
    text-align: center;
    border: 1px solid rgba(220, 53, 69, 0.2);
  }
  .error-message p {
    margin: 0;
  }

  .submit-button {
    width: 100%;
    padding: 0.85rem 1rem;
    font-size: 1rem;
    font-weight: 600;
    color: #fff;
    background-color: var(--primary-color, #007bff);
    border: none;
    border-radius: var(--border-radius, 0.375rem);
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
  }

  .submit-button:hover:not(:disabled) {
    background-color: #0056b3; /* Darker shade of primary */
  }

  .submit-button:disabled {
    background-color: #6c757d; /* --secondary-color */
    cursor: not-allowed;
  }

  .submit-button span { /* For loading text alignment */
    display: inline-block;
  }

  .alternative-action {
    text-align: center;
    margin-top: 2rem;
    font-size: 0.9rem;
  }

  .alternative-action p {
    color: var(--text-secondary, #6c757d);
    margin-bottom: 0;
  }

  .alternative-action a {
    color: var(--primary-color, #007bff);
    font-weight: 500;
    text-decoration: none;
  }

  .alternative-action a:hover {
    text-decoration: underline;
  }
</style>
