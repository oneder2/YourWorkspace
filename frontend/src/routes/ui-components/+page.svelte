<script lang="ts">
  import { 
    Alert, 
    Badge, 
    Button, 
    Card, 
    Input, 
    Select 
  } from '$lib/components/ui';

  // Sample data for Select component
  const countries = [
    { value: 'us', label: 'United States' },
    { value: 'ca', label: 'Canada' },
    { value: 'mx', label: 'Mexico' },
    { value: 'uk', label: 'United Kingdom' },
    { value: 'fr', label: 'France' },
  ];

  const countryGroups = [
    {
      label: 'North America',
      options: [
        { value: 'us', label: 'United States' },
        { value: 'ca', label: 'Canada' },
        { value: 'mx', label: 'Mexico' },
      ]
    },
    {
      label: 'Europe',
      options: [
        { value: 'uk', label: 'United Kingdom' },
        { value: 'fr', label: 'France' },
        { value: 'de', label: 'Germany' },
      ]
    }
  ];

  // Form state
  let name = '';
  let email = '';
  let country = '';
  let message = '';
  let formSubmitted = false;

  function handleSubmit() {
    formSubmitted = true;
    // In a real app, you would submit the form data to a server
    console.log({ name, email, country, message });
  }
</script>

<div class="max-w-7xl mx-auto px-4 py-12">
  <header class="mb-12 text-center">
    <h1 class="text-4xl font-bold mb-4">UI Component Library</h1>
    <p class="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
      A collection of reusable Tailwind CSS components for Svelte applications
    </p>
  </header>

  <!-- Buttons -->
  <section class="mb-16">
    <h2 class="text-2xl font-bold mb-6 pb-2 border-b border-gray-200 dark:border-gray-700">Buttons</h2>
    
    <div class="mb-8">
      <h3 class="text-xl font-semibold mb-4">Variants</h3>
      <div class="flex flex-wrap gap-4">
        <Button>Default</Button>
        <Button variant="primary">Primary</Button>
        <Button variant="secondary">Secondary</Button>
        <Button variant="success">Success</Button>
        <Button variant="danger">Danger</Button>
        <Button variant="warning">Warning</Button>
        <Button variant="info">Info</Button>
        <Button variant="outline">Outline</Button>
        <Button variant="ghost">Ghost</Button>
      </div>
    </div>

    <div class="mb-8">
      <h3 class="text-xl font-semibold mb-4">Sizes</h3>
      <div class="flex flex-wrap items-center gap-4">
        <Button variant="primary" size="sm">Small</Button>
        <Button variant="primary" size="md">Medium</Button>
        <Button variant="primary" size="lg">Large</Button>
      </div>
    </div>

    <div class="mb-8">
      <h3 class="text-xl font-semibold mb-4">States</h3>
      <div class="flex flex-wrap gap-4">
        <Button variant="primary" disabled>Disabled</Button>
        <Button variant="primary" loading>Loading</Button>
        <Button variant="primary" fullWidth>Full Width</Button>
      </div>
    </div>
  </section>

  <!-- Badges -->
  <section class="mb-16">
    <h2 class="text-2xl font-bold mb-6 pb-2 border-b border-gray-200 dark:border-gray-700">Badges</h2>
    
    <div class="mb-8">
      <h3 class="text-xl font-semibold mb-4">Variants</h3>
      <div class="flex flex-wrap gap-4">
        <Badge>Default</Badge>
        <Badge variant="primary">Primary</Badge>
        <Badge variant="secondary">Secondary</Badge>
        <Badge variant="success">Success</Badge>
        <Badge variant="danger">Danger</Badge>
        <Badge variant="warning">Warning</Badge>
        <Badge variant="info">Info</Badge>
        <Badge variant="outline">Outline</Badge>
      </div>
    </div>

    <div class="mb-8">
      <h3 class="text-xl font-semibold mb-4">Sizes</h3>
      <div class="flex flex-wrap items-center gap-4">
        <Badge variant="primary" size="sm">Small</Badge>
        <Badge variant="primary" size="md">Medium</Badge>
        <Badge variant="primary" size="lg">Large</Badge>
      </div>
    </div>
  </section>

  <!-- Cards -->
  <section class="mb-16">
    <h2 class="text-2xl font-bold mb-6 pb-2 border-b border-gray-200 dark:border-gray-700">Cards</h2>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <Card>
        <p>Simple card with just body content</p>
      </Card>
      
      <Card>
        <svelte:fragment slot="header">
          <h3 class="text-lg font-semibold">Card Title</h3>
        </svelte:fragment>
        
        <p>Card with header and body content</p>
      </Card>
      
      <Card>
        <svelte:fragment slot="header">
          <h3 class="text-lg font-semibold">Complete Card</h3>
        </svelte:fragment>
        
        <p class="mb-4">Card with header, body, and footer</p>
        
        <svelte:fragment slot="footer">
          <div class="flex justify-end">
            <Button variant="primary">Action</Button>
          </div>
        </svelte:fragment>
      </Card>
      
      <Card variant="primary">
        <svelte:fragment slot="header">
          <h3 class="text-lg font-semibold">Primary Card</h3>
        </svelte:fragment>
        
        <p>Card with primary variant</p>
      </Card>
      
      <Card variant="success" shadow="lg">
        <svelte:fragment slot="header">
          <h3 class="text-lg font-semibold">Success Card</h3>
        </svelte:fragment>
        
        <p>Card with success variant and large shadow</p>
      </Card>
    </div>
  </section>

  <!-- Alerts -->
  <section class="mb-16">
    <h2 class="text-2xl font-bold mb-6 pb-2 border-b border-gray-200 dark:border-gray-700">Alerts</h2>
    
    <div class="space-y-4">
      <Alert>Default alert message</Alert>
      <Alert variant="primary">Primary alert message</Alert>
      <Alert variant="success" title="Success">Operation completed successfully</Alert>
      <Alert variant="danger" title="Error" dismissible>Something went wrong. Please try again.</Alert>
      <Alert variant="warning" title="Warning" dismissible>Your account is about to expire</Alert>
      <Alert variant="info" title="Information">This is an informational message</Alert>
    </div>
  </section>

  <!-- Form Elements -->
  <section class="mb-16">
    <h2 class="text-2xl font-bold mb-6 pb-2 border-b border-gray-200 dark:border-gray-700">Form Elements</h2>
    
    <Card>
      <svelte:fragment slot="header">
        <h3 class="text-lg font-semibold">Contact Form Example</h3>
      </svelte:fragment>
      
      <form on:submit|preventDefault={handleSubmit} class="space-y-4">
        <Input 
          label="Name" 
          type="text" 
          placeholder="Enter your name" 
          required 
          bind:value={name}
        />
        
        <Input 
          label="Email" 
          type="email" 
          placeholder="Enter your email" 
          required 
          bind:value={email}
        />
        
        <Select 
          label="Country" 
          options={countries} 
          placeholder="Select your country" 
          bind:value={country}
        />
        
        <Input 
          label="Message" 
          type="textarea" 
          placeholder="Enter your message" 
          required 
          bind:value={message}
        />
        
        <div class="flex justify-end">
          <Button variant="primary" type="submit">Submit</Button>
        </div>
      </form>
      
      {#if formSubmitted}
        <Alert variant="success" class="mt-4">Form submitted successfully!</Alert>
      {/if}
    </Card>
  </section>
</div>
