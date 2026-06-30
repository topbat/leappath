---
name: Vibrant Career Flux
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#4a4455'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#7b7487'
  outline-variant: '#ccc3d8'
  surface-tint: '#732ee4'
  primary: '#630ed4'
  on-primary: '#ffffff'
  primary-container: '#7c3aed'
  on-primary-container: '#ede0ff'
  inverse-primary: '#d2bbff'
  secondary: '#a53b29'
  on-secondary: '#ffffff'
  secondary-container: '#fe7d66'
  on-secondary-container: '#711609'
  tertiary: '#00594b'
  on-tertiary: '#ffffff'
  tertiary-container: '#007462'
  on-tertiary-container: '#5cfedd'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#eaddff'
  primary-fixed-dim: '#d2bbff'
  on-primary-fixed: '#25005a'
  on-primary-fixed-variant: '#5a00c6'
  secondary-fixed: '#ffdad4'
  secondary-fixed-dim: '#ffb4a6'
  on-secondary-fixed: '#3f0300'
  on-secondary-fixed-variant: '#842415'
  tertiary-fixed: '#58fbda'
  tertiary-fixed-dim: '#2cdebf'
  on-tertiary-fixed: '#00201a'
  on-tertiary-fixed-variant: '#005143'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  display-lg:
    fontFamily: Quicksand
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Quicksand
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg-mobile:
    fontFamily: Quicksand
    fontSize: 28px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Quicksand
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Quicksand
    fontSize: 18px
    fontWeight: '500'
    lineHeight: '1.6'
  body-md:
    fontFamily: Quicksand
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '700'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 40px
  xl: 64px
  container-max: 1200px
  gutter: 24px
---

## Brand & Style

This design system is engineered for the next generation of professionals, prioritizing a "靈動輕盈" (Dynamic & Lightweight) aesthetic. It targets new graduates and creatives who view career searching not as a chore, but as an exploration of potential.

The visual direction blends **Modern Minimalism** with **Glassmorphism**. By using semi-transparent surfaces, soft backdrops, and floating elements, the UI feels breathable and less rigid than traditional corporate portals. The emotional response should be one of optimism and clarity, moving away from "industrial" layouts toward a social-media-inspired, fluid experience.

**Key Principles:**
- **Translucency:** Use layered transparency to maintain context and depth.
- **Vibrancy:** High-saturation accents against clean, expansive whites.
- **Softness:** Large radii and organic transitions to reduce visual friction.
- **Momentum:** Subtle gradients and floating shadows that suggest movement and progress.

## Colors

The palette is anchored by an energetic **Vivid Violet** (#7C3AED) that serves as the primary brand driver, symbolizing ambition and creativity. 

- **Primary (Vivid Violet):** Used for primary actions, progress indicators, and active states.
- **Secondary (Soft Coral):** Used for "Hot Jobs," alerts, and secondary call-to-actions to add warmth.
- **Tertiary (Fresh Mint):** Reserved for "Success" states, "Applied" badges, and soft background gradients.
- **Neutrals:** A slate-based neutral palette ensures high readability while avoiding the harshness of pure black.
- **Gradients:** Use a linear gradient from Primary to a lighter violet (80% opacity) for headers and hero cards to create the "vibrant" feel.

## Typography

We use **Quicksand** as the primary typeface. Its rounded terminals and open counters provide the "friendly" and "approachable" tone required for a modern job assistant. For smaller UI labels and functional data where clarity is paramount, we pair it with **Plus Jakarta Sans** for its exceptional legibility at small sizes.

**Usage Rules:**
- **Headlines:** Always Quicksand. Use Bold (700) for section headers to create clear hierarchy.
- **Body:** Use Medium (500) for job descriptions to ensure comfort during long reading sessions.
- **Labels:** Use Plus Jakarta Sans for button text, tags, and form labels to provide a subtle professional contrast to the rounded display text.

## Layout & Spacing

The layout utilizes a **12-column fluid grid** for desktop, transitioning to a **single-column vertical stack** for mobile. 

**Layout Philosophy:**
- **Generous Whitespace:** Use `lg` (40px) or `xl` (64px) padding between major sections to prevent information overload.
- **Card-Based Architecture:** All job listings, profile snippets, and toolkits are encapsulated in cards. 
- **Floating Elements:** Key actions (like "Quick Apply" or "Chat with Assistant") should use fixed positioning with high z-index and `md` (24px) safe-area margins from the screen edges.
- **Mobile Adjustments:** Gutters reduce to 16px on mobile, and horizontal padding for containers reduces to 20px.

## Elevation & Depth

This design system relies on **Glassmorphism** and **Ambient Shadows** rather than flat borders.

- **Level 1 (Base Cards):** White background with 80% opacity, a 1px white border at 20% opacity, and a subtle `0px 4px 20px rgba(124, 58, 237, 0.05)` shadow.
- **Level 2 (Hover/Active):** Increase opacity to 95%. Shadow deepens to `0px 10px 30px rgba(124, 58, 237, 0.12)`.
- **Glass Effect:** Use a `backdrop-filter: blur(12px)` for navigation bars and modal overlays to maintain a sense of lightness and depth.
- **Floating Buttons:** Use a saturated Primary shadow `0px 8px 24px rgba(124, 58, 237, 0.3)` to make them appear physically lifted from the page.

## Shapes

The shape language is consistently "extra-rounded" to reinforce the friendly brand personality.

- **Standard Elements:** Use `rounded-lg` (16px) for standard buttons and input fields.
- **Containers:** Large cards and modal containers use `rounded-xl` (24px).
- **Badges/Tags:** Use a full pill-shape (`rounded-full`) for "Remote," "Full-time," or "Entry Level" tags.
- **Avatars:** Always circular to contrast against the soft-rectangle grid of job cards.

## Components

### Buttons
- **Primary:** Gradient background (Violet to Light Violet), white text, 16px radius. Large horizontal padding (32px).
- **Secondary:** Ghost style. Transparent background with a 1.5px Violet border. 
- **Icon Buttons:** Circular with a soft-tinted background of the icon color (e.g., light violet for a violet icon).

### Cards
- **Job Card:** 24px padding, 24px radius. Features a prominent company logo on the left. The background should be slightly translucent glass if placed over a gradient background.

### Input Fields
- **Search Bar:** Large 24px radius. Soft shadow on focus, no heavy borders. Use an icon prefix (magnifying glass) with the Secondary Coral color for a pop of energy.

### Chips & Tags
- Used for skills (e.g., "Figma," "React"). Light gray or soft-tinted background with a Medium font weight. 

### Floating Action Button (FAB)
- "Ask Assistant" button positioned at the bottom right. Uses the primary gradient and a distinct "Sparkle" icon to denote AI capability.

### Progress Indicators
- Smooth, rounded bars using the Primary-to-Secondary gradient to show profile completion or application status.