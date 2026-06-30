<template>
  <div class="space-y-4">
    <div v-for="(item, idx) in items" :key="idx" class="rounded-card border border-border p-4 relative">
      <button class="absolute top-2 right-2 text-ink-soft/60 hover:text-danger" @click="items.splice(idx, 1)">
        <span class="material-symbols-outlined" style="font-size:20px">close</span>
      </button>
      <div class="grid grid-cols-2 gap-3">
        <label v-for="f in fields" :key="f.key" :class="f.key === textareaKey ? 'col-span-2' : ''" class="block">
          <span class="text-xs font-medium text-ink-soft mb-1 block">{{ f.label }}</span>
          <textarea v-if="f.key === textareaKey" v-model="item[f.key]" rows="3" class="lp-input"></textarea>
          <input v-else v-model="item[f.key]" class="lp-input" />
        </label>
      </div>
    </div>
    <button class="lp-btn-outline w-full" @click="add">
      <span class="material-symbols-outlined" style="font-size:18px">add</span>{{ addLabel }}
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  items: { type: Array, required: true },
  fields: { type: Array, required: true },
  addLabel: { type: String, default: '添加' },
  textareaKey: { type: String, default: '' },
})
function add() {
  const obj = {}
  props.fields.forEach((f) => (obj[f.key] = ''))
  props.items.push(obj)
}
</script>
