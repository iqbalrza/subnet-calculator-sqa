---
name: Precision Network System
colors:
  surface: '#faf9fd'
  surface-dim: '#dbd9dd'
  surface-bright: '#faf9fd'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f3f7'
  surface-container: '#efedf1'
  surface-container-high: '#e9e7eb'
  surface-container-highest: '#e3e2e6'
  on-surface: '#1a1b1e'
  on-surface-variant: '#414754'
  inverse-surface: '#2f3033'
  inverse-on-surface: '#f1f0f4'
  outline: '#727785'
  outline-variant: '#c1c6d6'
  surface-tint: '#005bc0'
  primary: '#005bbf'
  on-primary: '#ffffff'
  primary-container: '#1a73e8'
  on-primary-container: '#ffffff'
  inverse-primary: '#adc7ff'
  secondary: '#5b5f64'
  on-secondary: '#ffffff'
  secondary-container: '#dde0e6'
  on-secondary-container: '#5f6368'
  tertiary: '#076d2e'
  on-tertiary: '#ffffff'
  tertiary-container: '#2e8744'
  on-tertiary-container: '#ffffff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc7ff'
  on-primary-fixed: '#001a41'
  on-primary-fixed-variant: '#004493'
  secondary-fixed: '#dfe3e8'
  secondary-fixed-dim: '#c3c7cc'
  on-secondary-fixed: '#181c20'
  on-secondary-fixed-variant: '#43474c'
  tertiary-fixed: '#9cf7a7'
  tertiary-fixed-dim: '#81da8d'
  on-tertiary-fixed: '#002109'
  on-tertiary-fixed-variant: '#005320'
  background: '#faf9fd'
  on-background: '#1a1b1e'
  surface-variant: '#e3e2e6'
typography:
  display-lg:
    fontFamily: Roboto Flex
    fontSize: 36px
    fontWeight: '600'
    lineHeight: 44px
  display-lg-mobile:
    fontFamily: Roboto Flex
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  headline-lg:
    fontFamily: Roboto Flex
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  headline-md:
    fontFamily: Roboto Flex
    fontSize: 20px
    fontWeight: '500'
    lineHeight: 28px
  headline-sm:
    fontFamily: Roboto Flex
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 24px
  body-lg:
    fontFamily: Roboto Flex
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Roboto Flex
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Roboto Flex
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Roboto Flex
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-md:
    fontFamily: Roboto Flex
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  code-lg:
    fontFamily: JetBrains Mono
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 24px
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 20px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '400'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-mobile: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
  space-2xl: 3rem
---

## Brand & Style

This design system embodies an educational, utility-centric aesthetic inspired by modern, clean productivity software. It merges extreme clarity, utilitarian order, and approachable minimalism to transform complex networking concepts—such as binary subnet masks, CIDR blocks, and Variable Length Subnet Masking (VLSM)—into intuitive visual structures.

The target audience includes network engineering students, IT educators, systems administrators, and DevOps professionals who require rapid, error-free subnet allocations and visual breakdown of address spaces. 

### Visual Tenets
- **Clarity over Decoration:** Interfaces prioritize scan-ability, exact alignments, and minimal cognitive friction.
- **Structured Precision:** Dense technical data (e.g., bitwise operations, address pools) is framed by balanced whitespace, delicate structural dividing lines, and clear component hierarchies.
- **Productive Calm:** The interface maintains an airy, low-distraction white and cool gray foundation, utilizing concentrated functional color only to communicate status, bit splits, and interactive focus.

## Colors

The color palette centers on a crisp daylight presentation with high-contrast, accessible text hierarchy and functional color signaling.

### Core Swatches
- **Primary Interactive (`#1A73E8`):** Main interactive state, focused borders, active tab indicators, and primary action buttons.
  - Hover: `#1557B0`
  - Active: `#174EA6`
  - Container Tint: `#E8F0FE`
- **Secondary Neutral (`#5F6368`):** Supporting labels, inline helper copy, inactive icons, and structural metadata.
- **Semantic Success (`#137333`):** Validated routes, available network host blocks, and success banners.
  - Container Tint: `#E6F4EA`
- **Semantic Error & Warning (`#D93025`):** Invalid octet ranges, subnet overlaps, and CIDR prefix overflow errors.
  - Container Tint: `#FCE8E6`
- **Semantic Warning Yellow (`#F9AB00`):** Subnet space saturation alerts.
  - Container Tint: `#FEF7E0`

### Surface Hierarchy
- **Canvas Base:** `#FFFFFF` (Default viewport and raised dialog surface).
- **Surface Level 1:** `#F8F9FA` (Subtle module background, calculator canvas background).
- **Surface Level 2:** `#F1F3F4` (Code block chips, tabular headers, pill badges, and input fills).
- **Surface Outline:** `#DADCE0` (1px precise hairline borders).
- **Text Primary:** `#202124` (High legibility body text and data values).
- **Text Secondary:** `#5F6368` (Captions, column headers, and helper messages).
- **Text Disabled:** `#80868B`.

## Typography

Typography establishes a strict dual-track hierarchy: **Roboto Flex** commands textual flow, structural headings, and control actions, while **JetBrains Mono** delivers numerical and bitwise precision.

### Typographic Rules
- **Monospace Isolation:** All IP addresses (e.g., `192.168.1.0/24`), subnet masks (`255.255.255.0`), wildcards, broadcast addresses, hex values, and binary representations (`11111111.11111111.11111111.00000000`) must strictly render in `JetBrains Mono` (`code-lg`, `code-md`, or `code-sm`).
- **Binary Bit Splitting:** In binary breakdown charts, use `letterSpacing: "0.08em"` to give individual bits visual rhythm, highlighting the network and host boundary with color shifts rather than size shifts.
- **Numbers in Tables:** Monospaced formatting ensures numerical alignment across multi-row VLSM calculation tables, keeping decimal octets and CIDR ranges vertically aligned.

## Layout & Spacing

The layout is built on an adaptive 8pt modular grid (`0.5rem`), transitioning down to a 4pt micro-grid (`space-xs`) for dense calculations, badges, and inline status chips.

### Grid & Breakpoints
- **Desktop (≥ 1200px):** 12-column layout with `margin: 2rem` and `gutter: 1.5rem`. Max inner content width is capped at `1280px` for optimal scanning. A split-pane architecture is preferred: network parameters on the left (4–5 columns) and dynamic calculation breakdowns/VLSM visualizers on the right (7–8 columns).
- **Tablet (768px – 1199px):** 8-column layout with `margin: 1.5rem` and `gutter: 1rem`. Panels stack vertically into input, results summary, and detailed allocation blocks.
- **Mobile (< 768px):** 4-column layout with `margin: 1rem` and `gutter: 1rem`. Calculations display through horizontally scrollable tabular cards or stacked collapsible cards.

### Spacing Principles
- Forms maintain compact density with `space-sm` between label and input, and `space-md` between discrete form fields.
- Subnet visual blocks (e.g., hierarchical tree or block maps) utilize `space-xs` borders and gaps to preserve continuous spatial representation of memory or IP address space.

## Elevation & Depth

Depth in this design system is delicate and structured. It relies primarily on flat surfaces, crisp hairlines (`#DADCE0`), and layered ambient light shadows rather than dark structural drop shadows.

### Elevation Levels
- **Level 0 (Flat/Canvas):** Default surface `#FFFFFF` or `#F8F9FA`. No shadow. Bounded by 1px solid `#DADCE0` when separation is required.
- **Level 1 (Card / Rest State):** Elevated data containers, calculated result cards, and input panels.
  - Shadow: `0 1px 2px 0 rgba(60, 64, 67, 0.30), 0 1px 3px 1px rgba(60, 64, 67, 0.15)`
  - Surface: `#FFFFFF`
- **Level 2 (Hover / Floating Control):** Interactive calculation rows on hover, active dropdown panels, and floating network split buttons.
  - Shadow: `0 1px 3px 0 rgba(60, 64, 67, 0.30), 0 4px 8px 3px rgba(60, 64, 67, 0.15)`
- **Level 3 (Modal / Export Drawer):** Subnet export overlays, CIDR cheat sheet dialogs, and popovers.
  - Shadow: `0 2px 6px 2px rgba(60, 64, 67, 0.15), 0 8px 16px 4px rgba(60, 64, 67, 0.30)`

### Depth Rules
- Always use subtle `1px solid #DADCE0` borders on Level 1 cards to preserve contrast across displays.
- Floating helper tooltips use `#202124` text with `#FFFFFF` background or dark slate pill overlays (`#202124` with `#FFFFFF` text) with Level 2 elevation.

## Shapes

The design system maintains a modern geometry balanced between technical structure and approachable ergonomics.

### Corner Radius Standards
- **Containers & Cards:** `8px` (`0.5rem`) for compact result panels, scaling up to `12px` or `16px` (`1rem`) for primary workspace wrappers and major module containers.
- **Interactive Controls (Inputs, Standard Buttons):** `4px` (`0.25rem`) to `8px` (`0.5rem`) to ensure distinct click targets that resemble structured software tools.
- **Pills & Badges:** `9999px` (Full Pill) for CIDR labels (e.g., `/27`), usable host status, mask type indicators, and network classification chips (Class A, B, C, Private, Public).

## Components

### Buttons
- **Primary:** Background `#1A73E8`, text `#FFFFFF`, border `none`, radius `4px` or `8px`. Padding `8px 24px`. Hover state: `#1557B0`. Focused: subtle outer ring `0 0 0 2px #E8F0FE`.
- **Secondary (Tonal / Outlined):** Background `#FFFFFF`, 1px solid border `#DADCE0`, text `#1A73E8`. Hover: `#F8F9FA` with border `#1A73E8`.
- **Text / Action:** Background transparent, text `#1A73E8`, hover background `#F1F3F4`. Used for "Add Subnet Row", "Copy Mask", or "Expand Bitstream".

### Input Fields & Selectors
- **Structure:** Height `40px` or `48px`, border `1px solid #DADCE0`, background `#FFFFFF`, radius `4px` or `8px`, typography `code-md` for IP inputs.
- **Active / Focus:** Border changes to `2px solid #1A73E8`, inset outline offset `0px`.
- **Floating Labels / Prefix Decorators:** Fixed leading prefix (e.g., `IP:` or `/`) set in `#5F6368`. Monospaced segment styling for individual octet inputs when segmented mode is active.
- **Validation Messages:** Displayed immediately beneath inputs in `body-sm` with color `#D93025` alongside an inline warning icon.

### Chips & Badges
- **Pill Status Badges:** Border-radius `9999px`, padding `2px 10px`, font `code-sm` or `label-md`.
  - Primary CIDR: `#E8F0FE` background with `#1A73E8` text.
  - Usable Space: `#E6F4EA` background with `#137333` text.
  - Overlap / Error: `#FCE8E6` background with `#D93025` text.
  - Reserved Range: `#FEF7E0` background with `#B06000` text.

### Cards & Result Blocks
- Constructed with `#FFFFFF` background, `1px solid #DADCE0`, and Elevation Level 1.
- Clear structural division between header metadata and body computations via a horizontal `1px solid #F1F3F4` divider.
- Interior key-value pairs (e.g., `Usable Hosts: 62`, `Broadcast: 192.168.1.63`) use a two-column definition format: secondary gray labels on top, monospaced dark slate values beneath.

### Data Tables (VLSM Allocation Table)
- **Header:** `#F8F9FA` surface, `1px solid #DADCE0` bottom line, text `label-md` `#5F6368` uppercase.
- **Rows:** Alternating subtle row zebra striping is disallowed; use pure `#FFFFFF` rows with `1px solid #F1F3F4` row borders, highlighting entire rows with `#E8F0FE` on hover.
- **Numeric Cells:** Monospace aligned right or left-aligned with static character widths.

### Specialized Component: Binary Octet Visualizer
- A continuous horizontal bar split into 32 cells grouped into 4 bytes by `space-sm` gaps.
- Network bits represented by filled blue blocks (`#1A73E8` with `#FFFFFF` 1s).
- Subnetted bits represented by light blue blocks (`#E8F0FE` with `#1A73E8` 1s).
- Host bits represented by neutral light gray blocks (`#F1F3F4` with `#5F6368` 0s).
- Interactive drag or slider divider separating network prefix and host portions with real-time feedback.