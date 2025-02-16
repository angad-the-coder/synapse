<template>
  <div class="border-2 rounded-md border-gray-200 p-3 relative mt-4">
    <h2 class="text-gray-600 bg-white uppercase tracking-wide font-bold absolute -top-3 px-1">
      <slot name="title"></slot>
    </h2>
    <slot />
  </div>
</template>
<script setup lang="ts">

</script>
