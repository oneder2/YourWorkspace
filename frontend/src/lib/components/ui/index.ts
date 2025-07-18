/**
 * UI Component Library
 *
 * This file exports all UI components for easy importing.
 *
 * Usage:
 * ```svelte
 * <script>
 *   import { Button, Card, Alert, ThemeToggle } from '$lib/components/ui';
 * </script>
 *
 * <Card>
 *   <Alert variant="info">Welcome to our UI library!</Alert>
 *   <Button variant="primary">Get Started</Button>
 *   <ThemeToggle />
 * </Card>
 * ```
 */

export { default as Alert } from './Alert.svelte';
export { default as Badge } from './Badge.svelte';
export { default as BackgroundUploader } from './BackgroundUploader.svelte';
export { default as Button } from './Button.svelte';
export { default as Card } from './Card.svelte';
export { default as Input } from './Input.svelte';
export { default as Select } from './Select.svelte';
export { default as ThemeToggle } from './ThemeToggle.svelte';
