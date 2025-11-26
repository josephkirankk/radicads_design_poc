# Radic Pro — UI Design Guidelines

> **Version**: 1.0  
> **Last Updated**: November 2025  
> **Design System**: Tailwind CSS + Shadcn UI

---

## 1. Design Principles

### 1.1 Core Values

| Principle | Description |
|-----------|-------------|
| **Clean** | Minimal visual noise, generous whitespace, focused content |
| **Modern** | Contemporary aesthetics, smooth transitions, subtle shadows |
| **Professional** | Trust-inspiring, polished, consistent across all screens |
| **Intuitive** | Self-explanatory UI, minimal learning curve |
| **Fast** | Instant feedback, optimistic updates, skeleton loaders |

### 1.2 Design Philosophy

```
"Every pixel should serve a purpose. 
 If it doesn't help the user create better ads, remove it."
```

---

## 2. Color System

### 2.1 Primary Palette

```css
/* Brand Colors */
--primary: 220 90% 56%;        /* #3B82F6 - Blue */
--primary-foreground: 0 0% 100%;

/* Neutral Colors */
--background: 0 0% 100%;        /* White */
--foreground: 222 47% 11%;      /* Near black */

/* Surface Colors */
--card: 0 0% 100%;
--card-foreground: 222 47% 11%;

--muted: 210 40% 96%;           /* Light gray */
--muted-foreground: 215 16% 47%;

/* Accent Colors */
--accent: 210 40% 96%;
--accent-foreground: 222 47% 11%;
```

### 2.2 Semantic Colors

```css
/* Status Colors */
--success: 142 76% 36%;         /* #22C55E - Green */
--warning: 38 92% 50%;          /* #F59E0B - Amber */
--error: 0 84% 60%;             /* #EF4444 - Red */
--info: 199 89% 48%;            /* #0EA5E9 - Sky */

/* Interactive States */
--ring: 221 83% 53%;            /* Focus ring */
--border: 214 32% 91%;          /* Borders */
--input: 214 32% 91%;           /* Input borders */
```

### 2.3 Dark Mode (Future)

```css
/* Dark mode overrides */
.dark {
  --background: 222 47% 11%;
  --foreground: 210 40% 98%;
  --card: 222 47% 11%;
  --muted: 217 33% 17%;
  --border: 217 33% 17%;
}
```

---

## 3. Typography

### 3.1 Font Stack

```css
/* Primary Font: Inter */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Monospace (code) */
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;
```

### 3.2 Type Scale

| Element | Size | Weight | Line Height | Usage |
|---------|------|--------|-------------|-------|
| **h1** | 36px / 2.25rem | 800 | 1.2 | Page titles |
| **h2** | 30px / 1.875rem | 700 | 1.3 | Section headers |
| **h3** | 24px / 1.5rem | 600 | 1.35 | Card titles |
| **h4** | 20px / 1.25rem | 600 | 1.4 | Subsections |
| **body** | 16px / 1rem | 400 | 1.5 | Paragraph text |
| **body-sm** | 14px / 0.875rem | 400 | 1.5 | Secondary text |
| **caption** | 12px / 0.75rem | 500 | 1.4 | Labels, hints |

### 3.3 Tailwind Classes

```tsx
// Headings
<h1 className="text-4xl font-extrabold tracking-tight">Page Title</h1>
<h2 className="text-3xl font-bold tracking-tight">Section</h2>
<h3 className="text-2xl font-semibold">Card Title</h3>

// Body text
<p className="text-base text-foreground">Main text</p>
<p className="text-sm text-muted-foreground">Secondary text</p>
<span className="text-xs font-medium">Label</span>
```

---

## 4. Spacing & Layout

### 4.1 Spacing Scale

Use Tailwind's default spacing scale (base 4px):

| Token | Value | Usage |
|-------|-------|-------|
| `space-1` | 4px | Tight spacing |
| `space-2` | 8px | Icon gaps |
| `space-3` | 12px | Button padding |
| `space-4` | 16px | Card padding |
| `space-6` | 24px | Section gaps |
| `space-8` | 32px | Large gaps |
| `space-12` | 48px | Page sections |

### 4.2 Container Widths

```tsx
// Full-width with max constraint
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

// Content containers
<div className="max-w-4xl">  // Readable content
<div className="max-w-2xl">  // Forms, dialogs
```

### 4.3 Grid System

```tsx
// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <Card />
  <Card />
  <Card />
</div>

// Sidebar layout
<div className="flex">
  <aside className="w-64 shrink-0">Sidebar</aside>
  <main className="flex-1 min-w-0">Content</main>
</div>
```

---

## 5. Component Patterns

### 5.1 Buttons

```tsx
// Primary action
<Button>Generate Designs</Button>

// Secondary action
<Button variant="secondary">Save Draft</Button>

// Destructive action
<Button variant="destructive">Delete</Button>

// Ghost (subtle)
<Button variant="ghost" size="icon">
  <Settings className="h-4 w-4" />
</Button>

// With loading state
<Button disabled={isLoading}>
  {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
  Generate
</Button>
```

### 5.2 Cards

```tsx
<Card className="hover:shadow-md transition-shadow">
  <CardHeader>
    <CardTitle>Design Title</CardTitle>
    <CardDescription>Created 2 hours ago</CardDescription>
  </CardHeader>
  <CardContent>
    <img src={thumbnail} className="rounded-lg aspect-square object-cover" />
  </CardContent>
  <CardFooter className="flex justify-between">
    <Button variant="ghost" size="sm">Edit</Button>
    <Button size="sm">Export</Button>
  </CardFooter>
</Card>
```

### 5.3 Form Inputs

```tsx
<div className="space-y-4">
  <div className="space-y-2">
    <Label htmlFor="prompt">Describe your ad</Label>
    <Textarea
      id="prompt"
      placeholder="Instagram ad for summer sale, vibrant colors..."
      className="min-h-[100px] resize-none"
    />
    <p className="text-xs text-muted-foreground">
      Be specific about colors, style, and key elements
    </p>
  </div>

  <div className="space-y-2">
    <Label>Brand Kit</Label>
    <Select>
      <SelectTrigger>
        <SelectValue placeholder="Select a brand" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="brand1">VoltSound</SelectItem>
        <SelectItem value="brand2">TechGear</SelectItem>
      </SelectContent>
    </Select>
  </div>
</div>
```

### 5.4 Loading States

```tsx
// Skeleton for cards
<div className="space-y-3">
  <Skeleton className="h-48 w-full rounded-lg" />
  <Skeleton className="h-4 w-3/4" />
  <Skeleton className="h-4 w-1/2" />
</div>

// Spinner overlay
<div className="absolute inset-0 bg-background/80 flex items-center justify-center">
  <Loader2 className="h-8 w-8 animate-spin text-primary" />
</div>

// Progress indicator
<div className="space-y-2">
  <p className="text-sm">Generating designs...</p>
  <Progress value={progress} className="h-2" />
</div>
```

### 5.5 Empty States

```tsx
<div className="flex flex-col items-center justify-center py-12 text-center">
  <div className="rounded-full bg-muted p-4 mb-4">
    <Sparkles className="h-8 w-8 text-muted-foreground" />
  </div>
  <h3 className="text-lg font-semibold">No designs yet</h3>
  <p className="text-sm text-muted-foreground mt-1 max-w-sm">
    Create your first AI-powered ad design in seconds
  </p>
  <Button className="mt-4">
    <Plus className="mr-2 h-4 w-4" />
    Create Design
  </Button>
</div>
```

---

## 6. Page Layouts

### 6.1 Dashboard Layout

```tsx
export default function DashboardLayout({ children }) {
  return (
    <div className="min-h-screen bg-muted/30">
      {/* Top Navigation */}
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur">
        <div className="flex h-16 items-center px-6">
          <Logo />
          <nav className="ml-8 flex gap-6">
            <NavLink href="/designs">Designs</NavLink>
            <NavLink href="/brands">Brand Kits</NavLink>
          </nav>
          <div className="ml-auto flex items-center gap-4">
            <Button variant="ghost" size="icon">
              <Bell className="h-5 w-5" />
            </Button>
            <UserMenu />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="p-6">
        <div className="max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
}
```

### 6.2 Editor Layout

```tsx
export default function EditorLayout() {
  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Editor Toolbar */}
      <header className="h-14 border-b flex items-center px-4 gap-2">
        <Button variant="ghost" size="icon" asChild>
          <Link href="/designs"><ArrowLeft /></Link>
        </Button>
        <Separator orientation="vertical" className="h-6" />
        <EditorToolbar />
        <div className="ml-auto flex gap-2">
          <Button variant="outline">Save</Button>
          <Button>Export</Button>
        </div>
      </header>

      {/* Editor Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel: Blocks */}
        <aside className="w-64 border-r bg-muted/20 overflow-y-auto">
          <BlockPanel />
        </aside>

        {/* Canvas Area */}
        <main className="flex-1 flex items-center justify-center bg-muted/50 p-8">
          <div className="shadow-2xl">
            <FabricCanvas />
          </div>
        </main>

        {/* Right Panel: Properties */}
        <aside className="w-80 border-l bg-background overflow-y-auto">
          <PropertiesPanel />
        </aside>
      </div>
    </div>
  );
}
```

### 6.3 Prompt/Generation Page

```tsx
export default function GeneratePage() {
  return (
    <div className="max-w-3xl mx-auto py-12">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold">Create New Design</h1>
        <p className="text-muted-foreground mt-2">
          Describe your ad and let AI do the heavy lifting
        </p>
      </div>

      <Card className="p-6">
        <form className="space-y-6">
          {/* Prompt Input */}
          <div className="space-y-2">
            <Label>What do you want to create?</Label>
            <Textarea
              className="min-h-[120px]"
              placeholder="Instagram ad for Black Friday sale, 40% off electronics, dark premium theme with gold accents..."
            />
          </div>

          {/* Options Row */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Brand Kit</Label>
              <Select><SelectTrigger><SelectValue /></SelectTrigger></Select>
            </div>
            <div className="space-y-2">
              <Label>Creative Concept</Label>
              <Select><SelectTrigger><SelectValue /></SelectTrigger></Select>
            </div>
          </div>

          {/* Generate Button */}
          <Button className="w-full h-12 text-lg">
            <Sparkles className="mr-2 h-5 w-5" />
            Generate 3 Designs
          </Button>
        </form>
      </Card>

      {/* Prompt Tips */}
      <div className="mt-8 p-4 bg-muted/50 rounded-lg">
        <h3 className="font-medium mb-2">💡 Tips for great prompts:</h3>
        <ul className="text-sm text-muted-foreground space-y-1">
          <li>• Include the occasion or theme (Diwali, Black Friday)</li>
          <li>• Mention key copy (40% OFF, Free Shipping)</li>
          <li>• Describe the visual style (dark, minimal, vibrant)</li>
        </ul>
      </div>
    </div>
  );
}
```

---

## 7. Animations & Transitions

### 7.1 Standard Transitions

```css
/* Default transition for all interactive elements */
.transition-default {
  @apply transition-all duration-200 ease-out;
}

/* Hover effects */
.hover-lift {
  @apply transition-transform hover:-translate-y-0.5 hover:shadow-md;
}

/* Scale on press */
.press-scale {
  @apply active:scale-[0.98];
}
```

### 7.2 Page Transitions

```tsx
// Fade in on mount
<motion.div
  initial={{ opacity: 0, y: 10 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  {children}
</motion.div>
```

### 7.3 Loading Animations

```css
/* Pulse for skeleton */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Spin for loaders */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Shimmer for cards */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

---

## 8. Responsive Design

### 8.1 Breakpoints

| Breakpoint | Width | Usage |
|------------|-------|-------|
| `sm` | 640px | Large phones |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Large screens |

### 8.2 Mobile-First Patterns

```tsx
// Stack on mobile, side-by-side on desktop
<div className="flex flex-col md:flex-row gap-4">

// Hide on mobile
<div className="hidden md:block">

// Different padding per breakpoint
<div className="p-4 md:p-6 lg:p-8">

// Responsive text
<h1 className="text-2xl md:text-3xl lg:text-4xl">
```

---

## 9. Accessibility

### 9.1 Requirements

- **WCAG 2.1 AA** compliance minimum
- Keyboard navigation for all interactive elements
- Focus indicators visible and clear
- Color contrast ratio ≥ 4.5:1 for text
- Screen reader support (proper ARIA labels)

### 9.2 Implementation

```tsx
// Focus ring
<Button className="focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">

// Skip link
<a href="#main" className="sr-only focus:not-sr-only focus:absolute ...">
  Skip to content
</a>

// Accessible icon button
<Button variant="ghost" size="icon" aria-label="Settings">
  <Settings className="h-4 w-4" />
</Button>

// Form labels
<Label htmlFor="email">Email address</Label>
<Input id="email" type="email" aria-describedby="email-hint" />
<p id="email-hint" className="text-xs text-muted-foreground">
  We'll never share your email
</p>
```

---

## 10. Icon Guidelines

### 10.1 Icon Library

Use **Lucide React** for all icons:

```tsx
import { 
  Sparkles,    // AI generation
  Palette,     // Brand kit
  Image,       // Images
  Type,        // Text
  Download,    // Export
  Settings,    // Settings
  Plus,        // Add
  Trash2,      // Delete
  Eye,         // Show/preview
  EyeOff,      // Hide
  Lock,        // Lock
  Unlock,      // Unlock
  Loader2,     // Loading spinner
} from 'lucide-react';
```

### 10.2 Icon Sizes

| Context | Size | Class |
|---------|------|-------|
| Button icon | 16px | `h-4 w-4` |
| Inline with text | 16px | `h-4 w-4` |
| Panel icons | 20px | `h-5 w-5` |
| Empty state | 32px | `h-8 w-8` |
| Hero icons | 48px | `h-12 w-12` |

---

## 11. Editor-Specific UI

### 11.1 Canvas Chrome

```tsx
// Canvas container with zoom indicator
<div className="relative">
  {/* Zoom indicator */}
  <div className="absolute top-4 right-4 bg-background/90 rounded-md px-2 py-1 text-xs font-medium">
    {zoom}%
  </div>
  
  {/* Canvas with shadow */}
  <div className="bg-white shadow-2xl rounded-lg overflow-hidden">
    <canvas id="fabric-canvas" />
  </div>
</div>
```

### 11.2 Block Panel Item

```tsx
<div className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-muted cursor-pointer">
  <div className="w-8 h-8 rounded bg-primary/10 flex items-center justify-center">
    <Type className="h-4 w-4 text-primary" />
  </div>
  <div className="flex-1 min-w-0">
    <p className="text-sm font-medium truncate">Headline</p>
    <p className="text-xs text-muted-foreground truncate">Summer Sale 40% OFF</p>
  </div>
  <div className="flex gap-1">
    <Button variant="ghost" size="icon" className="h-6 w-6">
      <Eye className="h-3 w-3" />
    </Button>
    <Button variant="ghost" size="icon" className="h-6 w-6">
      <Lock className="h-3 w-3" />
    </Button>
  </div>
</div>
```

### 11.3 Properties Panel Section

```tsx
<div className="p-4 border-b">
  <h3 className="text-sm font-semibold mb-3">Typography</h3>
  <div className="space-y-3">
    <div className="grid grid-cols-2 gap-2">
      <Select>
        <SelectTrigger className="h-8 text-xs">
          <SelectValue placeholder="Font" />
        </SelectTrigger>
      </Select>
      <Select>
        <SelectTrigger className="h-8 text-xs">
          <SelectValue placeholder="Weight" />
        </SelectTrigger>
      </Select>
    </div>
    <div className="flex items-center gap-2">
      <Label className="text-xs w-12">Size</Label>
      <Slider className="flex-1" />
      <Input className="w-14 h-8 text-xs text-center" />
    </div>
  </div>
</div>
```

---

## 12. Brand Consistency Checklist

### Before Launch
- [ ] All buttons use consistent sizing
- [ ] Colors match the defined palette
- [ ] Typography follows the scale
- [ ] Spacing is consistent (multiples of 4px)
- [ ] All icons are from Lucide
- [ ] Loading states on all async actions
- [ ] Empty states for all list views
- [ ] Error states with helpful messages
- [ ] Focus states visible on all interactive elements
- [ ] Transitions are smooth and purposeful
