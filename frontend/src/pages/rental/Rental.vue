<template>
  <div>
    <PageHeader title="租房选址" subtitle="以公司为中心找房 · 通勤圈 · 预算计算 · 城市对比" />

    <div class="flex gap-1 mb-5 bg-surface-2 p-1 rounded-pill w-fit">
      <button v-for="t in tabs" :key="t.key" class="px-4 py-1.5 rounded-pill text-sm font-medium transition-all" :class="tab === t.key ? 'bg-surface text-primary shadow-card' : 'text-ink-soft'" @click="tab = t.key">{{ t.label }}</button>
    </div>

    <!-- 地图找房 -->
    <div v-show="tab === 'map'">
      <div class="lp-card p-4 mb-4 flex flex-wrap items-center gap-3">
        <label class="flex items-center gap-2 text-sm">
          <span class="text-ink-soft">公司</span>
          <select v-model="centerId" class="lp-input !w-52" @change="reload">
            <option v-for="c in centers" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </label>
        <label class="flex items-center gap-2 text-sm">
          <span class="text-ink-soft">通勤方式</span>
          <select v-model="mode" class="lp-input !w-28" @change="reload">
            <option value="walk">步行</option><option value="subway">地铁</option><option value="drive">驾车</option>
          </select>
        </label>
        <label class="flex items-center gap-2 text-sm flex-1 min-w-[200px]">
          <span class="text-ink-soft whitespace-nowrap">租金 ≤ {{ priceMax }}</span>
          <input type="range" min="1500" max="6000" step="500" v-model.number="priceMax" class="flex-1 accent-[rgb(var(--c-primary))]" @change="reload" />
        </label>
        <select v-model="roomType" class="lp-input !w-28" @change="reload">
          <option value="">全部户型</option><option value="studio">单间</option><option value="1room">一室</option><option value="2room">两室</option><option value="3room">三室</option>
        </select>
      </div>

      <div class="grid lg:grid-cols-2 gap-4">
        <div>
          <RentalMap v-if="center" :center="center" :listings="listings" :circles="circles" :size="460" @select="selected = $event" />
        </div>
        <div class="space-y-3 max-h-[460px] overflow-y-auto pr-1">
          <div v-if="circles.length" class="lp-card p-3 flex justify-around text-center">
            <div v-for="c in circles" :key="c.minutes"><p class="font-display font-bold text-primary">{{ c.count }}</p><p class="text-xs text-ink-soft">{{ c.minutes }}min 圈内</p></div>
          </div>
          <div v-for="l in listings" :key="l.id" class="lp-card p-3 flex gap-3 hover:shadow-card cursor-pointer" :class="selected?.id === l.id ? '!border-primary' : ''" @click="selected = l">
            <div class="w-16 h-16 rounded-btn bg-surface-2 flex items-center justify-center text-ink-soft/50 shrink-0"><span class="material-symbols-outlined" style="font-size:28px">apartment</span></div>
            <div class="flex-1 min-w-0">
              <p class="font-display font-bold text-ink text-sm line-clamp-1">{{ l.community_name }} · {{ roomLabel[l.room_type] }}</p>
              <p class="text-xs text-ink-soft">{{ l.area_sqm }}㎡ · {{ l.orientation }} · {{ rentLabel[l.rent_type] }}</p>
              <div class="flex items-center justify-between mt-1">
                <span class="font-display font-bold text-accent">¥{{ l.price_monthly }}</span>
                <span v-if="l.commute_minutes" class="lp-tag text-xs" :class="l.commute_minutes <= 20 ? 'bg-success/15 text-success' : 'bg-warning/15 text-warning'">通勤 {{ l.commute_minutes }}min</span>
              </div>
            </div>
          </div>
          <EmptyState v-if="!listings.length" icon="home" title="该条件下暂无房源" />
        </div>
      </div>
    </div>

    <!-- 预算计算器 -->
    <div v-show="tab === 'budget'" class="grid lg:grid-cols-2 gap-5">
      <div class="lp-card p-6">
        <h3 class="lp-section-title mb-4">预算计算器</h3>
        <Field label="税前月薪（元）"><input v-model.number="gross" type="number" class="lp-input" @input="calcBudget" /></Field>
        <p class="text-sm text-ink-soft mt-3">建议租金不超过税后收入的 30%。</p>
      </div>
      <div class="lp-card p-6" v-if="budget">
        <h3 class="lp-section-title mb-4">测算结果</h3>
        <div class="space-y-3">
          <InfoRow label="税后月收入（估算）" :value="`¥${budget.after_tax}`" />
          <InfoRow label="建议租金上限（30%）" :value="`¥${budget.recommended_rent_cap}`" highlight />
          <InfoRow label="水电网" :value="`¥${budget.other_expenses.utilities}`" />
          <InfoRow label="通勤" :value="`¥${budget.other_expenses.commute}`" />
          <InfoRow label="餐饮" :value="`¥${budget.other_expenses.food}`" />
          <InfoRow label="预计可结余" :value="`¥${budget.estimated_savings}`" highlight />
        </div>
      </div>
    </div>

    <!-- 城市对比 -->
    <div v-show="tab === 'city'" class="lp-card p-6 overflow-x-auto">
      <h3 class="lp-section-title mb-4">城市横向对比（薪资购买力 · 租金 · 净结余）</h3>
      <table class="w-full text-sm">
        <thead><tr class="text-left text-ink-soft border-b border-border">
          <th class="py-2 pr-4 font-medium">城市</th><th class="py-2 px-3">平均月薪</th><th class="py-2 px-3">平均租金</th><th class="py-2 px-3">生活成本</th><th class="py-2 px-3">净结余/月</th><th class="py-2 px-3">房源数</th>
        </tr></thead>
        <tbody>
          <tr v-for="(c, i) in cityData" :key="c.city" class="border-b border-border/60">
            <td class="py-3 pr-4 font-display font-bold text-ink">{{ i === 0 ? '🏆 ' : '' }}{{ c.city }}</td>
            <td class="py-3 px-3">¥{{ c.avg_salary }}</td>
            <td class="py-3 px-3">¥{{ c.avg_rent }}</td>
            <td class="py-3 px-3">¥{{ c.living_cost }}</td>
            <td class="py-3 px-3 font-bold" :style="{ color: c.net_savings > 0 ? 'rgb(var(--c-success))' : 'rgb(var(--c-danger))' }">¥{{ c.net_savings }}</td>
            <td class="py-3 px-3 text-ink-soft">{{ c.listing_count }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import RentalMap from '@/components/rental/RentalMap.vue'
import Field from '@/components/resume/Field.vue'
import InfoRow from '@/components/common/InfoRow.vue'

const tabs = [{ key: 'map', label: '地图找房' }, { key: 'budget', label: '预算计算器' }, { key: 'city', label: '城市对比' }]
const tab = ref('map')
const centers = ref([])
const centerId = ref('')
const mode = ref('subway')
const priceMax = ref(5000)
const roomType = ref('')
const listings = ref([])
const circles = ref([])
const selected = ref(null)
const gross = ref(30000)
const budget = ref(null)
const cityData = ref([])
const roomLabel = { studio: '单间', '1room': '一室', '2room': '两室', '3room': '三室', '4room+': '四室+' }
const rentLabel = { whole: '整租', share: '合租' }

const center = computed(() => centers.value.find((c) => c.id === centerId.value))

async function reload() {
  const c = center.value
  if (!c) return
  const p = new URLSearchParams({ center_lng: c.lng, center_lat: c.lat, mode: mode.value, price_max: priceMax.value, city: c.city })
  if (roomType.value) p.set('room_type', roomType.value)
  listings.value = await api.get(`/rental/listings?${p}`)
  circles.value = (await api.post('/rental/commute-circles', { center_lng: c.lng, center_lat: c.lat, mode: mode.value, city: c.city })).circles
}
async function calcBudget() { budget.value = await api.post('/rental/budget', { gross_monthly: gross.value }) }

onMounted(async () => {
  centers.value = await api.get('/rental/company-centers')
  if (centers.value.length) { centerId.value = centers.value[0].id; await reload() }
  await calcBudget()
  cityData.value = await api.get('/rental/city-compare')
})
</script>
