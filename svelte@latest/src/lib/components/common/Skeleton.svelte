<script lang="ts">
  // Props
  let { 
    width = '100%', 
    height = '1rem',
    rounded = 'md',
    animate = true,
    className = ''
  } = $props<{
    width?: string;
    height?: string;
    rounded?: 'none' | 'sm' | 'md' | 'lg' | 'xl' | 'full';
    animate?: boolean;
    className?: string;
  }>();

  // Rounded classes
  const roundedClasses = {
    'none': 'rounded-none',
    'sm': 'rounded-sm',
    'md': 'rounded',
    'lg': 'rounded-lg',
    'xl': 'rounded-xl',
    'full': 'rounded-full'
  };
</script>

<div 
  class="bg-gray-200 dark:bg-gray-700 {roundedClasses[rounded]} {animate ? 'animate-pulse' : ''} {className}"
  style="width: {width}; height: {height};"
></div>
