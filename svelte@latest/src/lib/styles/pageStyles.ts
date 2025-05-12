/**
 * 统一页面风格配置
 *
 * 这个文件定义了应用程序中所有页面的统一风格，包括颜色、边框、阴影等。
 * 通过集中管理这些样式，可以确保整个应用程序的视觉一致性。
 */

// 页面容器样式
export const pageContainer = 'max-w-7xl mx-auto px-4 py-4';

// 卡片基础样式
export const cardBase = 'rounded-lg shadow-md border overflow-hidden bg-white dark:bg-gray-800';

// 页面特定颜色方案
export const colorSchemes = {
  // Plan 页面 - 绿色主题
  plan: {
    bg: 'bg-green-50 dark:bg-green-900/30',
    border: 'border-green-200 dark:border-green-800',
    text: 'text-green-900 dark:text-green-100',
    icon: 'text-green-500',
    hover: 'hover:bg-green-100 dark:hover:bg-green-800/50',
    scrollbar: 'bg-green-500',
    button: {
      primary: 'bg-green-600 hover:bg-green-700 text-white',
      secondary: 'bg-green-100 hover:bg-green-200 text-green-800 dark:bg-green-800 dark:hover:bg-green-700 dark:text-green-100'
    }
  },

  // Doing 页面 - 蓝色主题
  doing: {
    bg: 'bg-blue-50 dark:bg-blue-900/30',
    border: 'border-blue-200 dark:border-blue-800',
    text: 'text-blue-900 dark:text-blue-100',
    icon: 'text-blue-500',
    hover: 'hover:bg-blue-100 dark:hover:bg-blue-800/50',
    scrollbar: 'bg-blue-500',
    button: {
      primary: 'bg-blue-600 hover:bg-blue-700 text-white',
      secondary: 'bg-blue-100 hover:bg-blue-200 text-blue-800 dark:bg-blue-800 dark:hover:bg-blue-700 dark:text-blue-100'
    }
  },

  // Done 页面 - 紫色主题
  done: {
    bg: 'bg-purple-50 dark:bg-purple-900/30',
    border: 'border-purple-200 dark:border-purple-800',
    text: 'text-purple-900 dark:text-purple-100',
    icon: 'text-purple-500',
    hover: 'hover:bg-purple-100 dark:hover:bg-purple-800/50',
    scrollbar: 'bg-purple-500',
    button: {
      primary: 'bg-purple-600 hover:bg-purple-700 text-white',
      secondary: 'bg-purple-100 hover:bg-purple-200 text-purple-800 dark:bg-purple-800 dark:hover:bg-purple-700 dark:text-purple-100'
    }
  },

  // 通用中性颜色 - 用于次要元素
  neutral: {
    bg: 'bg-gray-50 dark:bg-gray-800',
    border: 'border-gray-200 dark:border-gray-700',
    text: 'text-gray-900 dark:text-gray-100',
    icon: 'text-gray-500',
    hover: 'hover:bg-gray-100 dark:hover:bg-gray-700',
    scrollbar: 'bg-gray-400',
    button: {
      primary: 'bg-gray-600 hover:bg-gray-700 text-white',
      secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-800 dark:bg-gray-700 dark:hover:bg-gray-600 dark:text-gray-100'
    }
  }
};

// 布局配置
export const layouts = {
  // 两列布局 (1:3 比例)
  twoColumnOneThree: 'grid grid-cols-1 lg:grid-cols-4 gap-6',
  // 两列布局 (1:1 比例)
  twoColumnEqual: 'grid grid-cols-1 md:grid-cols-2 gap-6',
  // 三列布局
  threeColumn: 'grid grid-cols-1 md:grid-cols-3 gap-6'
};

// 列宽配置
export const columnSpans = {
  full: 'col-span-full',
  half: 'md:col-span-1',
  oneThird: 'md:col-span-1',
  twoThirds: 'md:col-span-2',
  oneFourth: 'lg:col-span-1',
  threeFourths: 'lg:col-span-3'
};

// 标题样式
export const headings = {
  h1: 'text-3xl font-bold mb-4 flex items-center',
  h2: 'text-xl font-semibold mb-4 flex items-center',
  h3: 'text-lg font-semibold mb-2'
};

// 滚动区域样式
export const scrollArea = {
  container: 'relative overflow-hidden',
  content: 'h-full overflow-y-auto',
  indicator: 'absolute top-0 bottom-0 w-1 opacity-50'
};

// 按钮样式
export const buttons = {
  icon: 'p-1 rounded-md focus:outline-none focus:ring-2',
  action: 'px-4 py-2 rounded-md font-medium text-sm transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2',
  small: 'px-3 py-1 text-sm rounded-md'
};

// 表单元素样式
export const formElements = {
  input: 'w-full p-2 border rounded-md focus:ring-2 focus:ring-offset-0 focus:outline-none',
  textarea: 'w-full p-2 border rounded-md focus:ring-2 focus:ring-offset-0 focus:outline-none',
  label: 'block text-sm font-medium mb-1'
};

// 辅助函数：组合样式类
export function combineClasses(...classes: string[]): string {
  return classes.filter(Boolean).join(' ');
}

// 辅助函数：获取页面样式
export function getPageStyle(pageName: 'plan' | 'doing' | 'done' | 'neutral'): any {
  return colorSchemes[pageName];
}
