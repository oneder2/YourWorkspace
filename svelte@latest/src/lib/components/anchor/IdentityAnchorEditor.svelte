<script lang="ts">
    import { onMount } from 'svelte';
    import { anchorStore } from '$lib/store/anchorStore';
    // Corrected import: UpdateUserProfilePayload comes from anchorService
    import type { UserProfileData, UpdateUserProfilePayload } from '$lib/services/anchorService';
    import type { ApiError } from '$lib/services/api';

    // Local state for form fields, initialized from the store
    let professionalTitle = $state('');
    let oneLinerBio = $state('');
    let skill = $state('');
    let summary = $state('');

    // Local state for form feedback
    let localIsLoading = $state(false); // For the save operation specifically
    let localErrorMessage = $state('');
    let localSuccessMessage = $state('');

    // Subscribe to the identityProfile part of the anchorStore
    let storeProfileData = $state<UserProfileData | null>(null);
    let storeIsLoading = $state(false);
    let storeError = $state<string | null>(null);

    // 使用 $effect 监听 anchorStore 的变化
    $effect(() => {
      const storeValue = $anchorStore;
      storeProfileData = storeValue.identityProfile.profile;
      storeIsLoading = storeValue.identityProfile.isLoading;
      storeError = storeValue.identityProfile.error;

      if (storeProfileData && !localIsLoading) {
        professionalTitle = storeProfileData.professional_title || '';
        oneLinerBio = storeProfileData.one_liner_bio || '';
        skill = storeProfileData.skill || '';
        summary = storeProfileData.summary || '';
      }
    });

    onMount(() => {
      if (!storeProfileData && !storeIsLoading && !storeError) {
        // The page hosting this component should ideally trigger the load.
        // anchorStore.loadIdentityProfile();
      }

      // 不需要取消订阅，因为我们使用的是 $effect
    });

    async function handleSaveChanges() {
      localIsLoading = true;
      localErrorMessage = '';
      localSuccessMessage = '';

      if (!professionalTitle.trim() && !oneLinerBio.trim() && !skill.trim() && !summary.trim()) {
        localErrorMessage = 'Please provide at least one field.';
        localIsLoading = false;
        return;
      }

      const payload: UpdateUserProfilePayload = {
        professional_title: professionalTitle.trim() || null,
        one_liner_bio: oneLinerBio.trim() || null,
        skill: skill.trim() || null,
        summary: summary.trim() || null,
      };

      try {
        const updatedProfile = await anchorStore.saveIdentityProfile(payload);
        if (updatedProfile) {
          localSuccessMessage = 'Profile updated successfully!';
          setTimeout(() => localSuccessMessage = '', 3000);
        } else {
          // Error message should be set by anchorStore if saveIdentityProfile returned null
          // Use $anchorStore for reactive access to the latest store value if needed here.
          localErrorMessage = $anchorStore.identityProfile.error || 'Failed to save profile. Please try again.';
        }
      } catch (error: any) {
        const apiError = error as ApiError;
        localErrorMessage = apiError?.message || 'An unexpected error occurred while saving.';
        console.error('IdentityAnchorEditor handleSubmit error:', error);
      } finally {
        localIsLoading = false;
      }
    }
  </script>

  <div class="identity-anchor-editor-card">
    {#if storeIsLoading && !storeProfileData}
      <div class="message loading-message">
        <p>Loading profile information...</p>
      </div>
    {:else if storeError && !storeProfileData}
      <div class="message error-message">
        <p>Error loading profile: {storeError}</p>
        <button class="retry-button" onclick={() => anchorStore.loadIdentityProfile()}>Try Again</button>
      </div>
    {:else}
      <form onsubmit={(e) => { e.preventDefault(); handleSaveChanges(); }} class="identity-form">
        <div class="form-section">
          <h3 class="section-title">Your Professional Identity</h3>
          <p class="section-description">Define your core professional standing. This helps anchor your activities and goals.</p>
        </div>

        <div class="form-group">
          <label for="professional-title">Professional Title</label>
          <input
            type="text"
            id="professional-title"
            bind:value={professionalTitle}
            placeholder="e.g., Senior Software Engineer, Product Manager, Aspiring Data Scientist"
            disabled={localIsLoading}
            maxlength="100"
          />
          <small class="field-hint">Your current or target professional role.</small>
        </div>

        <div class="form-group">
          <label for="one-liner-bio">One-Liner Bio / Professional Summary</label>
          <textarea
            id="one-liner-bio"
            bind:value={oneLinerBio}
            placeholder="e.g., Passionate about building scalable web applications and leading dynamic teams."
            rows="3"
            disabled={localIsLoading}
            maxlength="250"
          ></textarea>
          <small class="field-hint">A concise summary of who you are professionally (max 250 chars).</small>
        </div>

        <div class="form-group">
          <label for="skill">Skills</label>
          <textarea
            id="skill"
            bind:value={skill}
            placeholder="e.g., JavaScript, React, Node.js, Project Management"
            rows="2"
            disabled={localIsLoading}
            maxlength="250"
          ></textarea>
          <small class="field-hint">Your key skills and competencies (max 250 chars).</small>
        </div>

        <div class="form-group">
          <label for="summary">Detailed Summary</label>
          <textarea
            id="summary"
            bind:value={summary}
            placeholder="e.g., I have 5 years of experience in web development with a focus on frontend technologies..."
            rows="4"
            disabled={localIsLoading}
            maxlength="500"
          ></textarea>
          <small class="field-hint">A more detailed description of your professional background (max 500 chars).</small>
        </div>

        {#if localErrorMessage}
          <div class="message error-message" aria-live="assertive">
            <p>{localErrorMessage}</p>
          </div>
        {/if}

        {#if localSuccessMessage}
          <div class="message success-message" aria-live="polite">
            <p>{localSuccessMessage}</p>
          </div>
        {/if}

        <div class="form-actions">
          <button type="submit" class="submit-button" disabled={localIsLoading}>
            {#if localIsLoading}
              <span>Saving...</span>
            {:else}
              <span>Save Identity Profile</span>
            {/if}
          </button>
        </div>
      </form>
    {/if}
  </div>

  <style>
    .identity-anchor-editor-card {
      background-color: var(--card-bg, #ffffff);
      padding: 2rem 2.5rem;
      border-radius: var(--border-radius-xl, 0.75rem); /* Larger radius for a prominent card */
      box-shadow: var(--shadow-lg, 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05));
    }

    .form-section {
      margin-bottom: 2rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--border-color-light, #e9ecef);
    }
    .section-title {
      font-size: 1.4rem;
      font-weight: 600;
      color: var(--text-primary, #212529);
      margin-bottom: 0.3rem;
    }
    .section-description {
      font-size: 0.9rem;
      color: var(--text-secondary, #6c757d);
      margin-bottom: 0;
    }

    .identity-form .form-group {
      margin-bottom: 1.75rem;
    }

    .form-group label {
      display: block;
      margin-bottom: 0.6rem;
      font-weight: 500;
      color: var(--text-primary, #333);
      font-size: 0.95rem;
    }

    .form-group input[type="text"],
    .form-group textarea {
      width: 100%;
      padding: 0.8rem 1rem;
      border: 1px solid var(--border-color, #ced4da);
      border-radius: var(--border-radius-md, 0.5rem);
      font-size: 1rem;
      transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
      background-color: var(--input-bg-light, #f8f9fa);
    }

    .form-group input::placeholder,
    .form-group textarea::placeholder {
      color: var(--text-placeholder, #6c757d);
      opacity: 0.8;
    }

    .form-group input:focus,
    .form-group textarea:focus {
      border-color: var(--primary-color, #007bff);
      box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
      outline: none;
      background-color: #fff;
    }

    .form-group input:disabled,
    .form-group textarea:disabled {
      background-color: #e9ecef;
      opacity: 0.7;
      cursor: not-allowed;
    }

    .field-hint {
      display: block;
      font-size: 0.8rem;
      color: var(--text-muted, #6c757d);
      margin-top: 0.4rem;
    }

    .message {
      padding: 0.8rem 1.2rem;
      border-radius: var(--border-radius-md, 0.5rem);
      margin-top: 1.5rem;
      margin-bottom: 1rem;
      text-align: center;
      font-size: 0.9rem;
    }
    .message p { margin: 0; }

    .loading-message {
      background-color: rgba(23, 162, 184, 0.05);
      color: var(--info-color, #17a2b8);
      border: 1px solid rgba(23, 162, 184, 0.1);
    }
    .error-message {
      background-color: rgba(220, 53, 69, 0.05);
      color: var(--danger-color, #dc3545);
      border: 1px solid rgba(220, 53, 69, 0.1);
    }
    .success-message {
      background-color: rgba(40, 167, 69, 0.05);
      color: var(--success-color, #28a745);
      border: 1px solid rgba(40, 167, 69, 0.1);
    }

    .retry-button {
      padding: 0.5rem 1rem;
      font-size: 0.9rem;
      color: #fff;
      background-color: var(--primary-color, #007bff);
      border: none;
      border-radius: var(--border-radius, 0.375rem);
      cursor: pointer;
      transition: background-color 0.2s ease-in-out;
      margin-top: 0.75rem;
    }
    .retry-button:hover {
      background-color: #0056b3;
    }

    .form-actions {
      margin-top: 2rem;
      text-align: right;
    }

    .submit-button {
      padding: 0.75rem 1.5rem;
      font-size: 1rem;
      font-weight: 500;
      color: #fff;
      background-color: var(--primary-color, #007bff);
      border: none;
      border-radius: var(--border-radius-md, 0.5rem);
      cursor: pointer;
      transition: background-color 0.2s ease-in-out, box-shadow 0.15s ease-in-out;
    }

    .submit-button:hover:not(:disabled) {
      background-color: #0056b3;
      box-shadow: var(--shadow-sm, 0 2px 4px rgba(0,0,0,0.07));
    }

    .submit-button:disabled {
      background-color: var(--secondary-color, #6c757d);
      cursor: not-allowed;
      opacity: 0.65;
    }
  </style>
