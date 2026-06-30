---
name: Professional Authority
colors:
  surface: '#f9f9ff'
  surface-dim: '#d3daef'
  surface-bright: '#f9f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3ff'
  surface-container: '#e9edff'
  surface-container-high: '#e1e8fd'
  surface-container-highest: '#dce2f7'
  on-surface: '#141b2b'
  on-surface-variant: '#434654'
  inverse-surface: '#293040'
  inverse-on-surface: '#edf0ff'
  outline: '#737686'
  outline-variant: '#c3c5d7'
  surface-tint: '#1353d8'
  primary: '#003fb1'
  on-primary: '#ffffff'
  primary-container: '#1a56db'
  on-primary-container: '#d4dcff'
  inverse-primary: '#b5c4ff'
  secondary: '#555f6d'
  on-secondary: '#ffffff'
  secondary-container: '#d6e0f1'
  on-secondary-container: '#596372'
  tertiary: '#474a4d'
  on-tertiary: '#ffffff'
  tertiary-container: '#5f6265'
  on-tertiary-container: '#dbdee1'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b5c4ff'
  on-primary-fixed: '#00174d'
  on-primary-fixed-variant: '#003dab'
  secondary-fixed: '#d9e3f4'
  secondary-fixed-dim: '#bdc7d8'
  on-secondary-fixed: '#121c28'
  on-secondary-fixed-variant: '#3e4755'
  tertiary-fixed: '#e0e2e6'
  tertiary-fixed-dim: '#c4c7ca'
  on-tertiary-fixed: '#191c1f'
  on-tertiary-fixed-variant: '#44474a'
  background: '#f9f9ff'
  on-background: '#141b2b'
  surface-variant: '#dce2f7'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.25'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  sidebar-width: 280px
  gutter: 1.5rem
  margin-desktop: 2rem
  margin-mobile: 1rem
  unit-xs: 0.25rem
  unit-sm: 0.5rem
  unit-md: 1rem
  unit-lg: 1.5rem
  unit-xl: 2.5rem
---

## Brand & Style

The design system is engineered for a **Corporate / Modern** aesthetic, prioritizing reliability, efficiency, and authoritative guidance. It targets professional job seekers who require a tool that feels like a career partner rather than a casual utility. 

The visual narrative is built on the pillars of **clarity and structure**. By utilizing a restrained color palette, precise alignment, and generous white space, the UI reduces cognitive load, allowing users to focus on high-stakes career decisions. Every element is designed to feel intentional and stable, evoking an emotional response of trust and confidence.

## Colors

The color strategy centers on a **Deep Corporate Blue** (#1A56DB) as the primary anchor, symbolizing intelligence and professionalism. This is supported by a sophisticated range of Grays and Slates to create a hierarchy of information without overwhelming the user.

- **Primary:** Reserved for main actions, active states, and brand-critical indicators.
- **Secondary/Neutral:** Used for secondary navigation, iconography, and supporting text to ensure high legibility.
- **Surface & Background:** A clean, off-white background (#F9FAFB) provides subtle contrast against white (#FFFFFF) cards and containers, creating a "layered" effect that organizes content naturally.

## Typography

This design system utilizes **Inter** for all typographic roles to ensure maximum legibility and a systematic, utilitarian feel. Inter’s tall x-height and neutral character make it ideal for data-heavy job listings and complex application forms.

- **Headlines:** Use Semi-Bold (600) to Bold (700) weights with slightly tighter letter spacing to create a strong, authoritative presence.
- **Body Text:** Set at 16px (Medium) for primary reading, emphasizing a comfortable line height (1.5) to maintain focus during long sessions.
- **Labels:** Use Medium (500) or Semi-Bold (600) weights to distinguish metadata from body content. Small labels are occasionally uppercased for better scannability in dense interfaces.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy for Desktop to ensure a consistent experience across large monitors, transitioning to a fluid model for Mobile.

- **Desktop (1440px):** A 12-column grid with a fixed 280px left-hand sidebar for primary navigation. This creates a "Control Center" feel where the sidebar remains accessible while the main content area (max-width 1160px) reflows.
- **Tablet (1024px):** The sidebar collapses into a hamburger menu or a slim icon-only rail (72px) to prioritize content.
- **Mobile (640px):** A single-column flow with 1rem (16px) horizontal margins. Bottom navigation or a top-bar menu is used for core actions.
- **Spacing Rhythm:** Based on an 8px (0.5rem) scale to ensure mathematical harmony across all components.

## Elevation & Depth

Visual hierarchy is established through **Tonal Layers** and **Ambient Shadows**, avoiding heavy gradients or skeuomorphism.

- **Level 0 (Background):** #F9FAFB. The base canvas.
- **Level 1 (Cards/Surface):** #FFFFFF with a 1px border (#E5E7EB) and a very soft, diffused shadow (Y: 1px, Blur: 3px, Opacity: 0.05). Used for job cards and dashboard widgets.
- **Level 2 (Modals/Popovers):** #FFFFFF with a more pronounced shadow (Y: 10px, Blur: 15px, Opacity: 0.1) to indicate temporary overlay and focus.
- **Active State:** Elements like focused input fields or active sidebar items utilize a subtle 2px primary-colored left border or an inner glow to denote selection without disrupting the grid.

## Shapes

The design system employs a **Rounded** shape language (8px / 0.5rem base) to balance professional rigor with modern approachability.

- **Standard (0.5rem):** Used for buttons, input fields, and small cards.
- **Large (1rem):** Used for primary container cards and modals.
- **Extra Large (1.5rem):** Used sparingly for marketing elements or large image containers.
- **Pill (9999px):** Exclusively for status tags (e.g., "Full-time", "Remote") to distinguish them from actionable buttons.

## Components

### Buttons
- **Primary:** Solid #1A56DB with white text. High-contrast, 8px rounded corners.
- **Secondary:** White background with #E5E7EB border and #111827 text.
- **Ghost:** No border or background; text turns #1A56DB on hover. Use for tertiary actions like "Cancel."

### Input Fields
- **Standard:** 1px border (#D1D5DB). On focus, the border changes to #1A56DB with a subtle 3px semi-transparent blue halo.
- **Labels:** Positioned strictly above the field for maximum accessibility.

### Cards
- **Job Listings:** Structured with the job title in Headline-SM, company name in Body-SM (Slate), and metadata (location, salary) as Pills. 
- **Hover State:** Cards should slightly shift background color to #F3F4F6 or increase shadow depth to Level 2 to indicate interactivity.

### Selection Controls
- **Checkboxes & Radios:** Sharp, clear #1A56DB fill when active. No soft shadows; prioritize high-contrast visibility.

### Navigation Sidebar
- **Desktop:** Solid #FFFFFF with a subtle right border (#E5E7EB). Active links feature a #EFF6FF background and #1A56DB text for clear location awareness.