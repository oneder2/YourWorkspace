<script lang="ts">
    import { anchorStore } from '$lib/store/anchorStore';
    import type { CurrentFocusItem } from '$lib/services/anchorService';
    import { createEventDispatcher } from 'svelte';
  
    // Props: 接收一个 CurrentFocusItem 对象
    export let item: CurrentFocusItem;
  
    const dispatch = createEventDispatcher();
  
    // 用于编辑和删除操作的本地加载状态
    let isLoadingDelete = false;
    // let isEditing = false; // 用于控制编辑模态框或内联编辑的状态 (后续实现)
  
    // 处理删除操作
    async function handleDelete() {
      if (!item) return;
  
      // 可选：添加确认对话框
      const confirmed = confirm(`您确定要删除这个焦点项目 "${item.title}" 吗?`);
      if (!confirmed) {
        return;
      }
  
      isLoadingDelete = true;
      try {
        await anchorStore.deleteCurrentFocusItem(item.id);
        // store 更新后，列表会自动响应式地移除这个条目
        dispatch('deleted', { id: item.id }); // 如果父组件需要知道，可以派发事件
      } catch (error) {
        console.error(`删除焦点项目 ${item.id} 失败:`, error);
        // 可以派发错误事件或显示局部错误信息
        dispatch('actionError', { message: '删除失败，请重试。' });
      } finally {
        isLoadingDelete = false;
      }
    }
  
    // 处理编辑操作 (目前是占位符)
    function handleEdit() {
      console.log('编辑焦点项目:', item.id);
      // isEditing = true; // 未来用于打开编辑模态框
      alert(`编辑 "${item.title}" 的功能尚未实现。`);
      // dispatch('editRequest', item); // 派发编辑请求事件，父组件可以监听并打开模态框
    }
  
    // 格式化日期 (可选)
    function formatDate(dateString?: string | null): string {
      if (!dateString) return '未设置';
      try {
        // 假设日期格式为 YYYY-MM-DD，并且是本地时区
        const date = new Date(dateString + 'T00:00:00');
        return new Intl.DateTimeFormat('zh-CN', { // 使用中文格式
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        }).format(date);
      } catch (e) {
        return dateString; // 格式化失败则返回原始字符串
      }
    }
  
    // 根据 item.status 给状态文本添加不同的样式类 (可选)
    $: statusClass = item.status ? `status-${item.status.toLowerCase().replace(/\s+/g, '-')}` : 'status-unknown';
  
  </script>
  
  <div class="focus-item-card">
    <div class="focus-item-header">
      <h4 class="item-title">{item.title}</h4>
      {#if item.item_type}
        <span class="item-type-badge">{item.item_type}</span>
      {/if}
    </div>
  
    <div class="focus-item-body">
      {#if item.description}
        <p class="item-description">{item.description}</p>
      {/if}
  
      <div class="item-meta-details">
        {#if item.start_date}
          <span class="meta-info start-date" title="开始日期">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
            {formatDate(item.start_date)}
          </span>
        {/if}
        {#if item.status}
          <span class="meta-info item-status {statusClass}" title="状态">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path><path d="m9 12 2 2 4-4"></path></svg>
            {item.status}
          </span>
        {/if}
      </div>
    </div>
  
    <div class="focus-item-actions">
      <button
        class="action-button edit-button"
        on:click={handleEdit}
        title="编辑此焦点项目"
        aria-label="编辑焦点项目: {item.title}"
        disabled={isLoadingDelete}
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
        <span>编辑</span>
      </button>
      <button
        class="action-button delete-button"
        on:click={handleDelete}
        title="删除此焦点项目"
        aria-label="删除焦点项目: {item.title}"
        disabled={isLoadingDelete}
      >
        {#if isLoadingDelete}
          <span class="spinner small-spinner"></span>
          <span>删除中...</span>
        {:else}
          <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
          <span>删除</span>
        {/if}
      </button>
    </div>
  
    </div>
  
  <style>
    .focus-item-card {
      background-color: var(--card-bg, #ffffff);
      border: 1px solid var(--border-color-light, #e9ecef);
      border-radius: var(--border-radius-md, 0.375rem);
      padding: 1.25rem 1.5rem;
      margin-bottom: 1rem; /* 条目之间的间距 */
      box-shadow: var(--shadow-sm, 0 2px 4px rgba(0,0,0,0.05));
      transition: box-shadow 0.2s ease-in-out;
      display: flex;
      flex-direction: column;
    }
    .focus-item-card:hover {
      box-shadow: var(--shadow-md, 0 4px 8px rgba(0,0,0,0.07));
    }
  
    .focus-item-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start; /* 垂直方向顶部对齐 */
      margin-bottom: 0.75rem;
    }
  
    .item-title {
      font-size: 1.2rem;
      font-weight: 600;
      color: var(--text-heading, #2c3e50);
      margin: 0;
      word-break: break-word;
    }
  
    .item-type-badge {
      font-size: 0.75rem;
      font-weight: 500;
      padding: 0.25rem 0.6rem;
      border-radius: var(--border-radius-pill, 20px);
      background-color: var(--badge-info-bg, #e0e7ff); /* 示例颜色 */
      color: var(--badge-info-text, #4338ca); /* 示例颜色 */
      margin-left: 0.75rem;
      white-space: nowrap; /* 防止类型文本换行 */
    }
  
    .focus-item-body {
      margin-bottom: 1rem;
      font-size: 0.9rem;
      color: var(--text-body, #333);
      line-height: 1.6;
    }
  
    .item-description {
      margin: 0 0 0.75rem 0;
      white-space: pre-wrap; /* 保留描述中的换行 */
    }
  
    .item-meta-details {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem; /* 元信息之间的间距 */
      font-size: 0.8rem;
      color: var(--text-muted, #555);
    }
  
    .meta-info {
      display: inline-flex;
      align-items: center;
      padding: 0.2rem 0.4rem;
      border-radius: var(--border-radius-sm, 0.2rem);
      /* background-color: var(--meta-item-bg-light, #f4f4f5); */ /* 可以给每个元信息项一个轻微背景 */
    }
    .meta-info svg {
      margin-right: 0.4em;
      opacity: 0.8;
    }
    /* 可以为不同的状态添加特定的背景色和文本颜色 */
    .item-status.status-active { color: var(--success-color, #198754); font-weight: 500; }
    .item-status.status-on-hold { color: var(--warning-color, #ffc107); font-weight: 500; }
    /* ... 其他状态样式 ... */
  
  
    .focus-item-actions {
      margin-top: auto; /* 将操作按钮推到底部 */
      padding-top: 1rem; /* 与上方内容分隔 */
      border-top: 1px solid var(--border-color-extralight, #f1f1f1);
      display: flex;
      justify-content: flex-end; /* 将按钮靠右对齐 */
      gap: 0.75rem; /* 按钮之间的间距 */
    }
  
    .action-button {
      display: inline-flex;
      align-items: center;
      gap: 0.4em; /* 图标和文本之间的间距 */
      padding: 0.4rem 0.8rem;
      font-size: 0.85rem;
      font-weight: 500;
      border-radius: var(--border-radius, 0.25rem);
      cursor: pointer;
      transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
      border: 1px solid transparent;
    }
    .action-button svg {
      opacity: 0.9;
    }
  
    .edit-button {
      background-color: var(--button-edit-bg, #e0f2fe); /* 浅蓝色背景 */
      color: var(--button-edit-text, #0ea5e9);
      border-color: var(--button-edit-border, #bae6fd);
    }
    .edit-button:hover:not(:disabled) {
      background-color: #ccebfd;
      border-color: #99d5fc;
    }
  
    .delete-button {
      background-color: var(--button-delete-bg, #fee2e2); /* 浅红色背景 */
      color: var(--button-delete-text, #ef4444);
      border-color: var(--button-delete-border, #fecaca);
    }
    .delete-button:hover:not(:disabled) {
      background-color: #fdd8d8;
      border-color: #fca9a9;
    }
  
    .action-button:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  
    .spinner.small-spinner {
      width: 14px;
      height: 14px;
      border-width: 2px;
      /* animation: spin 0.8s linear infinite; (继承自全局或定义) */
    }
    /* 确保 spin 动画已在全局或父组件中定义 */
    @keyframes spin { to { transform: rotate(360deg); } }
  
  </style>
  