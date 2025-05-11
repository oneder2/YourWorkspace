/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{html,js,svelte,ts}', // Scan all relevant files in src for Tailwind classes
  ],
  theme: {
    extend: {
      colors: {
        // 品牌色 (Brand Colors) - 来自 fornt_css_color.txt 的建议
        'brand-primary': '#2563EB', // 示例: blue-600 (主要品牌色，用于关键交互)
        'brand-secondary': '#10B981', // 示例: emerald-500 (次要品牌色，可用于特定强调)

        // 中性色 (Neutral Colors) - 构成界面的基础
        // Tailwind 提供了丰富的 gray, slate, zinc, neutral, stone 系列，通常可以直接使用
        // 这里定义一些语义化的中性色，方便统一调用，并映射到Tailwind的色阶或自定义值
        'neutral-text-primary': '#1F2937',   // 主要文字颜色 (e.g., text-gray-800)
        'neutral-text-secondary': '#6B7280', // 次要文字颜色 (e.g., text-gray-500)
        'neutral-text-muted': '#9CA3AF',      // 更浅的文字，用于提示或禁用状态 (e.g., text-gray-400)
        
        'neutral-bg-main': '#F9FAFB',        // 页面主背景 (e.g., bg-gray-50)
        'neutral-bg-alt': '#F3F4F6',         // 备用或区块背景 (e.g., bg-gray-100)
        'neutral-bg-card': '#FFFFFF',        // 卡片背景 (e.g., bg-white)
        'neutral-bg-hover': '#EFF6FF',       // 鼠标悬停背景 (e.g., bg-blue-50 or a light gray)
        'neutral-bg-active': '#DBEAFE',      // 激活/选中背景 (e.g., bg-blue-100)

        'neutral-border-strong': '#D1D5DB', // 较明显的边框 (e.g., border-gray-300)
        'neutral-border-soft': '#E5E7EB',   // 较柔和的边框/分割线 (e.g., border-gray-200)
        'neutral-border-focus': '#3B82F6',  // 输入框等聚焦时的边框颜色 (e.g., border-blue-500)

        // 功能/语义色 (Functional/Semantic Colors)
        'functional-success': '#16A34A',      // 成功状态 (e.g., green-600 for text, green-500 for bg)
        'functional-success-bg': '#D1FAE5',   // 成功状态背景 (e.g., green-100)
        'functional-warning': '#F59E0B',      // 警告状态 (e.g., amber-500)
        'functional-warning-bg': '#FEF3C7',   // 警告状态背景 (e.g., amber-100)
        'functional-error': '#DC2626',        // 错误状态 (e.g., red-600)
        'functional-error-bg': '#FEE2E2',     // 错误状态背景 (e.g., red-100)
        'functional-info': '#3B82F6',         // 信息状态 (e.g., blue-500)
        'functional-info-bg': '#DBEAFE',      // 信息状态背景 (e.g., blue-100)

        // 区域强调色 (Section Accent Colors) - 来自 fornt_css_color.txt
        'accent-anchor': '#4F46E5',    // 身份锚点 (e.g., indigo-600)
        'accent-doing': '#0EA5E9',     // 正在做 (e.g., sky-500)
        'accent-done': '#10B981',      // 已做/成就 (e.g., emerald-500) - 与 brand-secondary 相同，可考虑区分或复用
        'accent-plan': '#8B5CF6',      // 打算做/未来计划 (e.g., violet-500)
      },
      fontFamily: {
        // 设置默认无衬线字体，Inter 是一个不错的现代选择
        sans: ['Inter', 'ui-sans-serif', 'system-ui', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', '"Noto Sans"', 'sans-serif', '"Apple Color Emoji"', '"Segoe UI Emoji"', '"Segoe UI Symbol"', '"Noto Color Emoji"'],
        // 如果需要，可以添加其他字体栈，例如衬线字体或等宽字体
        // serif: ['ui-serif', 'Georgia', 'Cambria', '"Times New Roman"', 'Times', 'serif'],
        // mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', '"Liberation Mono"', '"Courier New"', 'monospace'],
      },
      // 可以在这里扩展其他主题配置，如间距 (spacing), 圆角 (borderRadius), 阴影 (boxShadow) 等
      // 例如:
      // borderRadius: {
      //   'sm': '0.125rem', // 2px
      //   'DEFAULT': '0.25rem', // 4px
      //   'md': '0.375rem', // 6px
      //   'lg': '0.5rem', // 8px
      //   'xl': '0.75rem', // 12px
      //   '2xl': '1rem', // 16px
      //   'full': '9999px',
      // }
    },
  },
  plugins: [
    // 可以在这里引入 Tailwind CSS 插件，例如:
    // require('@tailwindcss/forms'),
    // require('@tailwindcss/typography'),
    // require('@tailwindcss/aspect-ratio'),
  ],
};
