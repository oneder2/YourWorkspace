// 1. 将 adapter-auto 更改为 adapter-static
import adapter from '@sveltejs/adapter-static'; 
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte'; // 您原有的功能，保持不变

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://kit.svelte.dev/docs/integrations#preprocessors
  // for more information about preprocessors.
  
  // 您的 vitePreprocess 配置保持原样，所有功能不受影响
  preprocess: vitePreprocess(),

  kit: {
    // 2. 配置 adapter-static 以生成用于单页应用（SPA）的静态文件
    adapter: adapter({
      pages: 'build',
      assets: 'build',
      fallback: 'index.html', // 这一行对于单页应用至关重要
      precompress: false,
      strict: true
    }),
    
    // 您原有的其他配置（如下面的注释）都保留
    // alias: {
    //   $lib: 'src/lib',
    // }
  }
};

export default config;
