<script lang="ts">
  import "../app.css";
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { page } from '$app/state'; // 更新从 $app/stores 到 $app/state
  import { isAuthenticated } from '$lib/store/authStore';
  import { initializeApp } from '$lib/utils/appInitializer';
  import { browser } from '$app/environment';

  let { children } = $props<{ children?: any }>();

  // 初始化应用程序
  onMount(() => {
    console.log('+layout.svelte: onMount called');
    initializeApp();
    console.log('+layout.svelte: initializeApp completed');

    // 处理路由保护和重定向 - 只在浏览器中执行
    handleRouteProtection();
    console.log('+layout.svelte: handleRouteProtection called');
  });

  // 监听认证状态和路由变化
  $effect(() => {
    if (browser && $isAuthenticated !== undefined) {
      handleRouteProtection();
    }
  });

  // 监听路径变化
  $effect(() => {
    if (browser) {
      handleRouteProtection();
    }
  });

  // 路由保护和重定向逻辑
  function handleRouteProtection() {
    if (!browser) {
      console.log('+layout.svelte: handleRouteProtection - Not in browser environment, returning');
      return; // 确保只在浏览器中执行
    }

    const currentPath = page.url.pathname;
    console.log('+layout.svelte: handleRouteProtection - Current path:', currentPath);
    console.log('+layout.svelte: handleRouteProtection - isAuthenticated:', $isAuthenticated);

    // 如果用户已登录但访问的是登录或注册页面，重定向到 doing 页面
    if ($isAuthenticated && (currentPath === '/login' || currentPath === '/register')) {
      console.log('+layout.svelte: User is authenticated and trying to access login/register, redirecting to /doing');
      goto('/doing');
      return;
    }

    // 如果路由不存在或无效，重定向到 doing 页面（如果已登录）或登录页面（如果未登录）
    if (!currentPath || currentPath === '/') {
      if ($isAuthenticated) {
        console.log('+layout.svelte: Empty path with authenticated user, redirecting to /doing');
        goto('/doing');
      } else {
        console.log('+layout.svelte: Empty path with unauthenticated user, redirecting to /login');
        goto('/login');
      }
      return;
    }

    // 检查是否是受保护的路由
    const protectedRoutes = ['/doing', '/done', '/plan', '/anchor'];
    const isProtectedRoute = protectedRoutes.some(route => currentPath.startsWith(route));

    if (isProtectedRoute) {
      console.log('+layout.svelte: Current path is a protected route:', currentPath);
      if (!$isAuthenticated) {
        console.log('+layout.svelte: User is not authenticated, but this will be handled by (app) layout');
      }
    } else {
      console.log('+layout.svelte: Current path is not a protected route:', currentPath);
    }

    // 注意：我们移除了未登录用户的重定向逻辑，因为这会与 (app) 布局中的逻辑冲突
    // 让 (app) 布局处理受保护路由的重定向
  }
</script>

{children}
