<script lang="ts">
    import { anchorStore } from '$lib/store/anchorStore';
    import type { CreateCurrentFocusPayload } from '$lib/services/anchorService';
    import type { ApiError } from '$lib/services/api';
  
    // 表单字段的本地状态
    let title: string = '';
    let item_type: string = ''; // 条目类型
    let description: string = '';
    let start_date: string = ''; // YYYY-MM-DD 格式
    let status: string = ''; // 状态
  
    // 表单反馈的本地状态
    let isLoading: boolean = false;
    let errorMessage: string = '';
    let successMessage: string = '';
  
    // 用于 item_type 和 status 的建议选项 (可以根据实际需求调整)
    const suggestedItemTypes: string[] = ['Project', 'Learning Goal', 'Skill Development', 'Research', 'Personal Growth'];
    const suggestedStatuses: string[] = ['Active', 'On Hold', 'Planning', 'Nearing Completion', 'Blocked'];
  
  
    async function handleSubmit() {
      if (!title.trim()) {
        errorMessage = 'Title is required for a focus item.';
        successMessage = '';
        return;
      }
  
      isLoading = true;
      errorMessage = '';
      successMessage = '';
  
      const payload: CreateCurrentFocusPayload = {
        title: title.trim(),
        item_type: item_type.trim() || undefined, // 发送 undefined 如果为空，让后端处理默认值或null
        description: description.trim() || undefined,
        start_date: start_date || undefined,
        status: status.trim() || undefined,
      };
  
      try {
        const newFocusItem = await anchorStore.addCurrentFocusItem(payload);
        if (newFocusItem) {
          successMessage = `Focus item "${newFocusItem.title}" added successfully!`;
          // 清空表单字段
          title = '';
          item_type = '';
          description = '';
          start_date = '';
          status = '';
          // 几秒后清除成功消息
          setTimeout(() => successMessage = '', 3000);
        } else {
          // 如果 anchorStore.addCurrentFocusItem 返回 null 并且设置了错误
          errorMessage = $anchorStore.currentFocus.error || 'Failed to add focus item. Please try again.';
        }
      } catch (error: any) {
        // 这个 catch 块可能冗余，如果 store 已经处理了错误
        const apiError = error as ApiError;
        errorMessage = apiError?.message || 'An unexpected error occurred while adding the focus item.';
        console.error('FocusForm handleSubmit error:', error);
      } finally {
        isLoading = false;
      }
    }
  
    function getCurrentDateString(): string {
      const today = new Date();
      const year = today.getFullYear();
      const month = (today.getMonth() + 1).toString().padStart(2, '0');
      const day = today.getDate().toString().padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
  </script>
  
  <div class="focus-form-card">
    <form on:submit|preventDefault={handleSubmit} class="focus-form">
      <h3 class="form-title">Add New Focus Item</h3>
      <p class="form-subtitle">What are you currently concentrating on?</p>
  
      <div class="form-group">
        <label for="focus-title">Title <span class="required-asterisk">*</span></label>
        <input
          type="text"
          id="focus-title"
          bind:value={title}
          placeholder="e.g., Master SvelteKit, Launch New Product Feature"
          required
          disabled={isLoading}
          maxlength="150"
        />
      </div>
  
      <div class="form-group">
        <label for="focus-item-type">Item Type (e.g., Project, Learning)</label>
        <input
          type="text"
          id="focus-item-type"
          bind:value={item_type}
          placeholder="Project, Learning Goal, Skill Development..."
          list="suggested-item-types"
          disabled={isLoading}
          maxlength="50"
        />
        <datalist id="suggested-item-types">
          {#each suggestedItemTypes as type}
            <option value={type}></option>
          {/each}
        </datalist>
      </div>
  
      <div class="form-group">
        <label for="focus-description">Description</label>
        <textarea
          id="focus-description"
          bind:value={description}
          placeholder="Briefly describe this focus item, its goals, or context."
          rows="3"
          disabled={isLoading}
        ></textarea>
      </div>
  
      <div class="form-row">
        <div class="form-group form-group-half">
          <label for="focus-start-date">Start Date</label>
          <input
            type="date"
            id="focus-start-date"
            bind:value={start_date}
            min={getCurrentDateString()} disabled={isLoading}
          />
        </div>
  
        <div class="form-group form-group-half">
          <label for="focus-status">Status</label>
          <input
            type="text"
            id="focus-status"
            bind:value={status}
            placeholder="Active, On Hold, Planning..."
            list="suggested-statuses"
            disabled={isLoading}
            maxlength="50"
          />
          <datalist id="suggested-statuses">
            {#each suggestedStatuses as stat}
              <option value={stat}></option>
            {/each}
          </datalist>
        </div>
      </div>
  
      {#if errorMessage}
        <div class="message error-message" aria-live="assertive">
          <p>{errorMessage}</p>
        </div>
      {/if}
  
      {#if successMessage}
        <div class="message success-message" aria-live="polite">
          <p>{successMessage}</p>
        </div>
      {/if}
  
      <button type="submit" class="submit-button" disabled={isLoading}>
        {#if isLoading}
          <span>Adding Focus...</span>
        {:else}
          <span>Add Focus Item</span>
        {/if}
      </button>
    </form>
  </div>
  
  <style>
    .focus-form-card {
      background-color: var(--card-bg-light, #fdfdff); /* 稍浅的卡片背景 */
      padding: 1.75rem 2.25rem;
      border-radius: var(--border-radius-lg, 0.5rem);
      box-shadow: var(--shadow-md, 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06));
      margin-bottom: 2rem;
      max-width: 650px;
      margin-left: auto;
      margin-right: auto;
    }
  
    .form-title {
      font-size: 1.6rem;
      font-weight: 600;
      color: var(--text-heading, #1a202c);
      margin-bottom: 0.25rem;
      text-align: left;
    }
    .form-subtitle {
      font-size: 0.95rem;
      color: var(--text-secondary, #555);
      margin-bottom: 1.75rem;
      text-align: left;
    }
  
    .focus-form .form-group {
      margin-bottom: 1.4rem;
    }
  
    .form-group label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: 500;
      color: var(--text-label, #333);
      font-size: 0.9rem;
    }
  
    .required-asterisk {
      color: var(--danger-color, #dc3545);
      margin-left: 0.2rem;
    }
  
    .form-group input[type="text"],
    .form-group input[type="date"],
    .form-group textarea {
      width: 100%;
      padding: 0.75rem 1rem;
      border: 1px solid var(--border-color-medium, #ccc);
      border-radius: var(--border-radius, 0.375rem);
      font-size: 1rem;
      transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
      background-color: var(--input-bg, #fff);
    }
    
    .form-group input::placeholder,
    .form-group textarea::placeholder {
      color: var(--text-placeholder, #999);
      opacity: 0.8;
    }
  
    .form-group input:focus,
    .form-group textarea:focus {
      border-color: var(--primary-color, #007bff);
      box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
      outline: none;
    }
  
    .form-group input:disabled,
    .form-group textarea:disabled {
      background-color: #e9ecef;
      opacity: 0.7;
      cursor: not-allowed;
    }
  
    .form-row {
      display: flex;
      gap: 1.5rem;
      margin-bottom: 1.4rem;
    }
    .form-group-half {
      flex: 1;
    }
  
    .message {
      padding: 0.8rem 1.2rem;
      border-radius: var(--border-radius, 0.375rem);
      margin-top: 1.25rem;
      margin-bottom: 1rem;
      text-align: center;
      font-size: 0.9rem;
    }
    .message p { margin: 0; }
  
    .error-message {
      background-color: rgba(220, 53, 69, 0.1);
      color: var(--danger-color, #dc3545);
      border: 1px solid rgba(220, 53, 69, 0.2);
    }
  
    .success-message {
      background-color: rgba(40, 167, 69, 0.1);
      color: var(--success-color, #28a745);
      border: 1px solid rgba(40, 167, 69, 0.2);
    }
  
    .submit-button {
      width: 100%;
      padding: 0.85rem 1rem;
      font-size: 1rem;
      font-weight: 500;
      color: #fff;
      background-color: var(--primary-color, #007bff);
      border: none;
      border-radius: var(--border-radius, 0.375rem);
      cursor: pointer;
      transition: background-color 0.2s ease-in-out, box-shadow 0.15s ease-in-out;
    }
  
    .submit-button:hover:not(:disabled) {
      background-color: #0056b3;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
  
    .submit-button:disabled {
      background-color: var(--secondary-color, #6c757d);
      cursor: not-allowed;
      opacity: 0.65;
    }
  </style>
  