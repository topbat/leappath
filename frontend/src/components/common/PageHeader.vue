<template>
  <div class="flex items-start justify-between gap-4 mb-6">
    <div>
      <div v-if="back" class="mb-2">
        <button class="inline-flex items-center gap-1 text-sm text-ink-soft hover:text-primary" @click="$router.back()">
          <span class="material-symbols-outlined" style="font-size:18px">arrow_back</span> 返回
        </button>
      </div>
      <h1 class="font-display text-2xl font-bold text-ink tracking-tight">{{ title }}</h1>
      <p v-if="subtitle" class="text-ink-soft mt-1">{{ subtitle }}</p>
    </div>
    <div class="flex items-center gap-2 shrink-0">
      <slot name="actions" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  back: { type: Boolean, default: false },
})
</script>
