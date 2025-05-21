<script lang="ts">
  import Skeleton from '$lib/components/common/Skeleton.svelte';

  // Props
  let { count = 5 } = $props<{
    count?: number;
  }>();

  // Create an array of the specified count
  const items = Array.from({ length: count }, (_, i) => i);
</script>

<div class="space-y-4">
  {#each items as item (item)}
    <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
      <div class="flex justify-between items-start">
        <div class="flex-1">
          <Skeleton width="70%" height="1.25rem" className="mb-2" />
          <Skeleton width="40%" height="0.875rem" />
        </div>
        <div class="flex space-x-2">
          <Skeleton width="1.5rem" height="1.5rem" rounded="full" />
          <Skeleton width="1.5rem" height="1.5rem" rounded="full" />
        </div>
      </div>
    </div>
  {/each}
</div>
