<script lang="ts">
    import { goto } from '$app/navigation';
    import { authService, type RegisterPayload } from '$lib/services/authService';
    import type { ApiError } from '$lib/services/api'; // Corrected import for ApiError
    import { isAuthenticated } from '$lib/store/authStore';
    import { onMount } from 'svelte';

    let username = '';
    let email = '';
    let password = '';
    let confirmPassword = '';

    let errorMessage = '';
    let successMessage = '';
    let isLoading = false;

    onMount(() => {
      const unsubscribe = isAuthenticated.subscribe(authenticated => {
        if (authenticated) {
          goto('/doing');
        }
      });
      return unsubscribe;
    });

    async function handleRegister() {
      isLoading = true;
      errorMessage = '';
      successMessage = '';

      console.log('Register form submitted with:', { username, email, passwordLength: password.length });

      // Client-side validation
      if (password !== confirmPassword) {
        errorMessage = 'Passwords do not match.';
        isLoading = false;
        return;
      }

      if (password.length < 8) {
        errorMessage = 'Password must be at least 8 characters long.';
        isLoading = false;
        return;
      }

      if (!username || username.trim().length < 3) {
        errorMessage = 'Username must be at least 3 characters long.';
        isLoading = false;
        return;
      }

      if (!email || !email.includes('@')) {
        errorMessage = 'Please enter a valid email address.';
        isLoading = false;
        return;
      }

      const payload: RegisterPayload = {
        username: username.trim(),
        email: email.trim(),
        password
      };

      console.log('Sending registration request with payload:', {
        username: payload.username,
        email: payload.email,
        passwordLength: payload.password.length
      });

      try {
        // 添加更多详细的日志记录
        console.log('Calling authService.registerUser with payload');
        const response = await authService.registerUser(payload);
        console.log('Registration successful:', response);
        successMessage = response.message + " You can now log in.";
        username = '';
        email = '';
        password = '';
        confirmPassword = '';

        // 注册成功后延迟跳转到登录页面
        setTimeout(() => {
          goto('/login');
        }, 2000);
      } catch (error: any) {
        console.error('Registration error (raw):', error);

        // 尝试提取有意义的错误信息
        const apiError = error as ApiError;
        console.error('Registration error details:', {
          status: apiError.status,
          message: apiError.message,
          data: apiError.data
        });

        // 更详细的错误处理
        if (apiError.status === 409) {
          // 处理冲突错误（用户名或邮箱已存在）
          if (apiError.data && apiError.data.error && apiError.data.error.includes('Username')) {
            errorMessage = '用户名已被占用，请尝试其他用户名。';
          } else if (apiError.data && apiError.data.error && apiError.data.error.includes('Email')) {
            errorMessage = '该邮箱已注册，请直接登录或使用其他邮箱。';
          } else {
            errorMessage = '用户名或邮箱已被占用，请尝试其他信息。';
          }
        } else if (apiError.data && apiError.data.message) {
          errorMessage = apiError.data.message;
        } else if (apiError.data?.error) {
          let messages: string[] = [];
          if (typeof apiError.data.error === 'object') {
            for (const key in apiError.data.error) {
              messages.push(`${key}: ${apiError.data.error[key]}`);
            }
            errorMessage = messages.join('; ');
          } else {
            errorMessage = apiError.data.error;
          }
        } else if (apiError.message) {
          errorMessage = apiError.message;
        } else {
          errorMessage = '注册过程中发生意外错误，请稍后重试。';
        }
      } finally {
        isLoading = false;
      }
    }
  </script>

  <div class="register-container">
    <div class="register-card">
      <h1 class="card-title">Create Account</h1>
      <p class="card-subtitle">Join us! Fill in the details below to get started.</p>

      <form on:submit|preventDefault={handleRegister} class="register-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            bind:value={username}
            required
            placeholder="your_username"
            disabled={isLoading}
          />
        </div>

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
            placeholder="•••••••• (min. 8 characters)"
            disabled={isLoading}
          />
        </div>

         <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input
            type="password"
            id="confirmPassword"
            bind:value={confirmPassword}
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

        {#if successMessage}
          <div class="success-message">
            <p>{successMessage}</p>
          </div>
        {/if}

        <button type="submit" class="submit-button" disabled={isLoading}>
          {#if isLoading}
            <span>Creating Account...</span>
          {:else}
            <span>Sign Up</span>
          {/if}
        </button>
      </form>

      <div class="alternative-action">
        <p>
          Already have an account?
          <a href="/login">Log in here</a>
        </p>
      </div>
    </div>
  </div>

  <style>
    /* Styles are very similar to login page, with minor adjustments */
    .register-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 80vh;
      padding: 2rem 1rem;
      background-color: var(--light-color, #f4f7f9);
    }

    .register-card {
      background-color: #ffffff;
      padding: 2.5rem 2rem;
      border-radius: var(--border-radius, 0.375rem);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1), 0 5px 10px rgba(0, 0, 0, 0.04);
      width: 100%;
      max-width: 450px; /* Slightly wider for more fields */
    }

    .card-title {
      font-size: 2rem;
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

    .register-form .form-group {
      margin-bottom: 1.25rem; /* Slightly less margin for more fields */
    }

    .form-group label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: 500;
      color: var(--text-primary, #333);
    }

    .form-group input {
      width: 100%;
      padding: 0.75rem 1rem;
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
      background-color: rgba(220, 53, 69, 0.1);
      color: var(--danger-color, #dc3545);
      padding: 0.75rem 1rem;
      border-radius: var(--border-radius, 0.375rem);
      margin-bottom: 1.25rem;
      text-align: center;
      border: 1px solid rgba(220, 53, 69, 0.2);
    }
    .error-message p {
      margin: 0;
    }

    .success-message {
      background-color: rgba(40, 167, 69, 0.1); /* --success-color with opacity */
      color: var(--success-color, #28a745);
      padding: 0.75rem 1rem;
      border-radius: var(--border-radius, 0.375rem);
      margin-bottom: 1.25rem;
      text-align: center;
      border: 1px solid rgba(40, 167, 69, 0.2);
    }
    .success-message p {
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
      background-color: #0056b3;
    }

    .submit-button:disabled {
      background-color: #6c757d;
      cursor: not-allowed;
    }

    .submit-button span {
      display: inline-block;
    }

    .alternative-action {
      text-align: center;
      margin-top: 1.5rem; /* Adjusted margin */
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
