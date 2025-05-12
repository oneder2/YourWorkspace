<script lang="ts">
  /**
   * SvgIcon Component
   * 
   * A standardized way to use SVG icons throughout the application.
   * This component handles loading SVGs from the static assets folder.
   * 
   * Usage:
   * ```svelte
   * <SvgIcon name="todo" size="24" />
   * ```
   */
  import { SvgIcons } from '$lib/utils/svgUtils';
  
  // Component props
  let {
    name,
    size = 24,
    color = 'currentColor',
    class: className = '',
    ...rest
  } = $props<{
    name: string;
    size?: string | number;
    color?: string;
    class?: string;
    [key: string]: any;
  }>();
  
  // Determine the SVG source URL
  let svgSrc = '';
  
  // Check if the name is a predefined icon
  if (name in SvgIcons) {
    svgSrc = SvgIcons[name as keyof typeof SvgIcons];
  } else {
    // Otherwise, assume it's a direct path or a custom icon name
    svgSrc = name.includes('/') ? name : `/images/icons/${name}.svg`;
  }
  
  // Convert size to string with 'px' if it's a number
  const sizeValue = typeof size === 'number' ? `${size}px` : size;
</script>

<img
  src={svgSrc}
  width={sizeValue}
  height={sizeValue}
  alt=""
  class={className}
  style={color !== 'currentColor' ? `color: ${color};` : ''}
  {...rest}
/>
