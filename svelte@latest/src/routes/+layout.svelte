<script lang="ts">
  import "../app.css";
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';
  import { isAuthenticated } from '$lib/store/authStore';
  import { initializeApp } from '$lib/utils/appInitializer';
  import { browser } from '$app/environment';

  // 初始化应用程序
  onMount(() => {
    initializeApp();

    // 处理路由保护和重定向 - 只在浏览器中执行
    handleRouteProtection();
  });

  // 监听认证状态和路由变化
  $: if (browser && ($isAuthenticated !== undefined || $page.url.pathname)) {
    handleRouteProtection();
  }

  // 路由保护和重定向逻辑
  function handleRouteProtection() {
    if (!browser) return; // 确保只在浏览器中执行

    const currentPath = $page.url.pathname;

    // 如果用户已登录但访问的是登录或注册页面，重定向到 doing 页面
    if ($isAuthenticated && (currentPath === '/login' || currentPath === '/register')) {
      goto('/doing');
    }

    // 如果用户未登录且访问的不是登录或注册页面，重定向到登录页面
    if (!$isAuthenticated && currentPath !== '/login' && currentPath !== '/register') {
      goto('/login');
    }

    // 如果路由不存在或无效，重定向到 doing 页面（如果已登录）或登录页面（如果未登录）
    if (!currentPath || currentPath === '/') {
      if ($isAuthenticated) {
        goto('/doing');
      } else {
        goto('/login');
      }
    }
  }
</script>

<slot></slot>
