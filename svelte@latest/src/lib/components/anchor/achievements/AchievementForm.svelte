<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import { get } from 'svelte/store'; // Import get
    import type { Achievement, AchievementCreateDto, AchievementUpdateDto } from '$lib/services/achievementService';
    import { achievementStore } from '$lib/store/achievementStore'; // achievementStore is an object containing multiple stores
  
    // Props
    export let achievement: Achievement | null = null;
    
    // Local state for form fields
    let title: string = achievement?.title || '';
    let description: string = achievement?.description || '';
    let quantifiable_results: string = achievement?.quantifiable_results || '';
    let core_skills_input: string = achievement?.core_skills_json?.join(', ') || '';
    let date_achieved: string = achievement?.date_achieved || ''; // YYYY-MM-DD
  
    let formError: string | null = null;
    let formSuccess: string | null = null;
    let internalIsLoading: boolean = false; // Local loading state for the form operations
  
    const dispatch = createEventDispatcher();
  
    // Extract the specific store for isLoading
    const isLoadingStore = achievementStore.isLoading; 
    // Now, auto-subscribe to this specific store
    $: storeIsLoading = $isLoadingStore; 
  
    $: {
      if (achievement) {
        title = achievement.title || '';
        description = achievement.description || '';
        quantifiable_results = achievement.quantifiable_results || '';
        core_skills_input = achievement.core_skills_json?.join(', ') || '';
        date_achieved = achievement.date_achieved || '';
        formError = null; // Clear previous errors when achievement changes
        formSuccess = null;
      } else {
        // Reset for create mode if achievement becomes null or is initially null
        title = '';
        description = '';
        quantifiable_results = '';
        core_skills_input = '';
        date_achieved = '';
      }
    }
  
    const handleSubmit = async () => {
      formError = null;
      formSuccess = null;
      internalIsLoading = true;
  
      if (!title.trim()) {
        formError = '标题不能为空。';
        internalIsLoading = false;
        return;
      }
  
      const core_skills_json = core_skills_input
        .split(',')
        .map(skill => skill.trim())
        .filter(skill => skill !== '');
  
      if (achievement && achievement.id) {
        const achievementData: AchievementUpdateDto = {
          title,
          description: description || null,
          quantifiable_results: quantifiable_results || null,
          core_skills_json: core_skills_json.length > 0 ? core_skills_json : undefined,
          date_achieved: date_achieved || null,
        };
        try {
          const updated = await achievementStore.updateAchievement(achievement.id, achievementData);
          if (updated) {
            formSuccess = '成就更新成功！';
            dispatch('save', updated);
          } else {
            formError = get(achievementStore.error) || '更新成就失败。';
          }
        } catch (e: any) {
          formError = e.message || '更新时发生未知错误。';
        }
      } else {
        const achievementData: AchievementCreateDto = {
          title,
          description: description || null,
          quantifiable_results: quantifiable_results || null,
          core_skills_json: core_skills_json.length > 0 ? core_skills_json : undefined,
          date_achieved: date_achieved || null,
        };
        try {
          const created = await achievementStore.addAchievement(achievementData);
          if (created) {
            formSuccess = '成就添加成功！';
            dispatch('save', created);
            resetForm();
          } else {
            formError = get(achievementStore.error) || '添加成就失败。';
          }
        } catch (e: any) {
          formError = e.message || '添加时发生未知错误。';
        }
      }
      internalIsLoading = false;
    };
  
    const resetForm = () => {
      title = '';
      description = '';
      quantifiable_results = '';
      core_skills_input = '';
      date_achieved = '';
      formError = null;
      // formSuccess = null; // Decide if success message should also be cleared on reset
    };
  
    const handleCancel = () => {
      if (achievement) {
          dispatch('cancel'); // For modal to handle
      } else {
          resetForm();
          formSuccess = null;
      }
    }
  
  </script>
  
  <form on:submit|preventDefault={handleSubmit} class="space-y-6 p-4 bg-white dark:bg-gray-800 shadow-md rounded-lg">
    <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
      {achievement ? '编辑成就' : '添加新成就'}
    </h3>
  
    {#if formError}
      <div class="p-3 mb-4 text-sm text-red-700 bg-red-100 rounded-lg dark:bg-red-200 dark:text-red-800" role="alert">
        <span class="font-medium">错误：</span> {formError}
      </div>
    {/if}
    {#if formSuccess}
      <div class="p-3 mb-4 text-sm text-green-700 bg-green-100 rounded-lg dark:bg-green-200 dark:text-green-800" role="alert">
        <span class="font-medium">成功：</span> {formSuccess}
      </div>
    {/if}
  
    <div>
      <label for="title-achv" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">标题 <span class="text-red-500">*</span></label>
      <input type="text" id="title-achv" bind:value={title} required
             class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
             placeholder="例如：完成XX项目第一阶段">
    </div>
  
    <div>
      <label for="description-achv" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">描述</label>
      <textarea id="description-achv" rows="3" bind:value={description}
                class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="详细描述这个成就..."></textarea>
    </div>
  
    <div>
      <label for="quantifiable_results-achv" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">可量化成果</label>
      <input type="text" id="quantifiable_results-achv" bind:value={quantifiable_results}
             class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
             placeholder="例如：提高效率20%，节省成本1万元">
    </div>
  
    <div>
      <label for="core_skills_input-achv" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">核心技能 (逗号分隔)</label>
      <input type="text" id="core_skills_input-achv" bind:value={core_skills_input}
             class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
             placeholder="例如：沟通, 领导力, Svelte">
    </div>
    
    <div>
      <label for="date_achieved-achv" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">达成日期</label>
      <input type="date" id="date_achieved-achv" bind:value={date_achieved}
             class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
    </div>
  
    <div class="flex justify-end space-x-3 pt-4">
      <button type="button" on:click={handleCancel}
              class="py-2.5 px-5 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700">
        {achievement ? '取消' : '重置'}
      </button>
      <button type="submit" disabled={internalIsLoading || storeIsLoading}
              class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 disabled:opacity-50">
        {#if internalIsLoading || storeIsLoading}
          <svg aria-hidden="true" role="status" class="inline w-4 h-4 me-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
            <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0492C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
          </svg>
          处理中...
        {:else}
          {achievement ? '保存更改' : '添加成就'}
        {/if}
      </button>
    </div>
  </form>
  