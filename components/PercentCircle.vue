<!-- eslint-disable tailwindcss/no-custom-classname -->
<template>
  <div class="relative flex items-center justify-center">
    <svg viewBox="0 0 36 36" class="aspect-square w-full">
      <path
        class="text-gray-200 dark:text-slate-700"
        d="M18 2.0845
      a 15.9155 15.9155 0 0 1 0 31.831
      a 15.9155 15.9155 0 0 1 0 -31.831"
        fill="none"
        stroke="currentColor"
        :stroke-width="strokeWidth"
        stroke-linecap="round"
      />
      <path
        v-if="dashArray !== undefined"
        class="pct-circle transition-[stroke-dasharray,color] duration-300" 
        :class="color"
        d="M18 2.0845
        a 15.9155 15.9155 0 0 1 0 31.831
        a 15.9155 15.9155 0 0 1 0 -31.831"
        fill="none"
        stroke="currentColor"
        :stroke-width="strokeWidth"
        stroke-linecap="round"
        :stroke-dasharray="dashArray"
      />
    </svg>
    <div class="absolute text-center font-medium">
      <slot />
    </div>
  </div>
</template>
<script setup lang="ts">
const props = defineProps<{
  percent: number | undefined;
}>();
const strokeWidth = 2;
const dashArray = computed(() => {
  const pct = props.percent;
  if (pct == null || isNaN(pct) || !isFinite(pct) || pct === 0) {
    return undefined;
  }
  const adjustedPct = pct < 1 ? ((pct * 100) - strokeWidth) : (pct * 100);
  return `${adjustedPct < 0 ? 0 : adjustedPct}, 100`;
});
const color = computed(() => {
  if (props.percent == null) { return "text-green-500" }
  const colorRanges = [
    { max: 0.16, color: "text-green-500" },
    { max: 0.33, color: "text-lime-500" },
    { max: 0.50, color: "text-yellow-500" },
    { max: 0.66, color: "text-amber-500" },
    { max: 0.83, color: "text-orange-500" },
    { max: 1.00, color: "text-red-500" }
  ];

  // @ts-ignore
  const color = colorRanges.find(range => props.percent! <= range.max);

  return color == null ? "text-red-500" : color.color;
})
</script>
<style scoped>
.pct-circle {
  animation: build-up 0.5s ease-out;
}
@keyframes build-up {
  0% {
    stroke-dasharray: 0 100;
  }
}
</style>
