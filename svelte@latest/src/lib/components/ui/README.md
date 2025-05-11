# UI Component Library

A collection of reusable Tailwind CSS components for Svelte applications.

## Components

### Button

A versatile button component with various styles and sizes.

```svelte
<script>
  import { Button } from '$lib/components/ui';
</script>

<Button>Default Button</Button>
<Button variant="primary">Primary Button</Button>
<Button variant="outline" size="sm">Small Outline Button</Button>
<Button variant="danger" disabled>Disabled Danger Button</Button>
<Button variant="success" loading>Loading Button</Button>
<Button variant="primary" fullWidth>Full Width Button</Button>
```

#### Props

- `variant`: 'default' | 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'info' | 'outline' | 'ghost'
- `size`: 'sm' | 'md' | 'lg'
- `type`: HTML button type
- `disabled`: boolean
- `loading`: boolean
- `fullWidth`: boolean
- `class`: Additional CSS classes

### Badge

A badge component for displaying status, counts, or labels.

```svelte
<script>
  import { Badge } from '$lib/components/ui';
</script>

<Badge>Default</Badge>
<Badge variant="primary">Primary</Badge>
<Badge variant="success" size="lg">Success</Badge>
<Badge variant="danger" rounded="full">Error</Badge>
```

#### Props

- `variant`: 'default' | 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'info' | 'outline'
- `size`: 'sm' | 'md' | 'lg'
- `rounded`: 'none' | 'sm' | 'md' | 'lg' | 'xl' | 'full'
- `class`: Additional CSS classes

### Card

A card component with header, body, and footer sections.

```svelte
<script>
  import { Card, Button } from '$lib/components/ui';
</script>

<Card>
  <p>Simple card with just body content</p>
</Card>

<Card>
  <svelte:fragment slot="header">
    <h3>Card Title</h3>
  </svelte:fragment>
  
  <p>Card body content</p>
  
  <svelte:fragment slot="footer">
    <Button>Action</Button>
  </svelte:fragment>
</Card>
```

#### Props

- `variant`: 'default' | 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'info'
- `padding`: boolean
- `shadow`: 'none' | 'sm' | 'md' | 'lg' | 'xl'
- `rounded`: 'none' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | 'full'
- `border`: boolean
- `class`: Additional CSS classes

### Alert

An alert component for displaying messages, warnings, or errors.

```svelte
<script>
  import { Alert } from '$lib/components/ui';
</script>

<Alert>Default alert message</Alert>
<Alert variant="primary" title="Information">This is an informational message</Alert>
<Alert variant="danger" dismissible>This is a dismissible error message</Alert>
```

#### Props

- `variant`: 'default' | 'primary' | 'secondary' | 'danger' | 'success' | 'warning' | 'info'
- `title`: string
- `dismissible`: boolean
- `icon`: boolean
- `class`: Additional CSS classes

#### Events

- `dismiss`: Fired when the alert is dismissed

### Input

An input component with various styles and states.

```svelte
<script>
  import { Input } from '$lib/components/ui';
  let value = '';
</script>

<Input placeholder="Enter your name" bind:value />
<Input type="email" label="Email Address" required />
<Input type="password" label="Password" error="Password is too short" />
<Input type="text" label="Username" hint="Choose a unique username" />
<Input type="text" disabled value="Disabled input" />
```

#### Props

- `type`: HTML input type
- `value`: string | number
- `placeholder`: string
- `label`: string
- `id`: string
- `name`: string
- `disabled`: boolean
- `readonly`: boolean
- `required`: boolean
- `error`: string
- `hint`: string
- `fullWidth`: boolean
- `class`: Additional CSS classes

#### Events

- `input`: Fired when the input value changes
- `change`: Fired when the input value is committed

### Select

A select component for dropdown selection.

```svelte
<script>
  import { Select } from '$lib/components/ui';
  let value = '';
  
  const options = [
    { value: 'us', label: 'United States' },
    { value: 'ca', label: 'Canada' },
    { value: 'mx', label: 'Mexico' }
  ];
</script>

<Select label="Choose a country" {options} bind:value />
```

#### Props

- `value`: string | number
- `options`: Array of option objects or option group objects
- `label`: string
- `id`: string
- `name`: string
- `placeholder`: string
- `disabled`: boolean
- `required`: boolean
- `error`: string
- `hint`: string
- `fullWidth`: boolean
- `class`: Additional CSS classes

#### Events

- `change`: Fired when the select value changes

## Usage

Import components from the library:

```svelte
<script>
  import { Button, Card, Alert } from '$lib/components/ui';
</script>

<Card>
  <Alert variant="info">Welcome to our UI library!</Alert>
  <Button variant="primary">Get Started</Button>
</Card>
```

Visit the `/ui-components` route to see all components in action.
