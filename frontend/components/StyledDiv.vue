<template>
  <div class="border-2 rounded-md border-gray-200 p-3 pt-4 relative mt-6 mb-4" :class="center && 'flex flex-col items-center'">
    <h2 class="text-gray-600 bg-white uppercase tracking-wide font-bold absolute -top-3 px-1" :class="center && 'left-1/2 -translate-x-1/2'">
      <slot name="title"></slot>
    </h2>
    <slot />
  </div>
</template>
<script setup lang="ts">
defineProps<{
  center?: boolean;
}>();
</script>
