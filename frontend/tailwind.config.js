/** 双主题：颜色用 CSS 变量（RGB 通道）实现，支持 Tailwind 透明度修饰符。 */
function withAlpha(varName) {
  return ({ opacityValue }) =>
    opacityValue === undefined
      ? `rgb(var(${varName}))`
      : `rgb(var(${varName}) / ${opacityValue})`
}

export default {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        bg: withAlpha('--c-bg'),
        surface: withAlpha('--c-surface'),
        'surface-2': withAlpha('--c-surface-2'),
        border: withAlpha('--c-border'),
        ink: withAlpha('--c-ink'),
        'ink-soft': withAlpha('--c-ink-soft'),
        primary: withAlpha('--c-primary'),
        'primary-soft': withAlpha('--c-primary-soft'),
        'on-primary': withAlpha('--c-on-primary'),
        accent: withAlpha('--c-accent'),
        mint: withAlpha('--c-mint'),
        success: withAlpha('--c-success'),
        warning: withAlpha('--c-warning'),
        danger: withAlpha('--c-danger'),
      },
      borderRadius: {
        card: 'var(--radius-card)',
        btn: 'var(--radius-btn)',
        pill: '9999px',
      },
      fontFamily: {
        display: 'var(--font-display)',
        body: 'var(--font-body)',
      },
      boxShadow: {
        card: 'var(--shadow-card)',
        lift: 'var(--shadow-lift)',
      },
    },
  },
  plugins: [],
}
