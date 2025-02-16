<template>
  <div class="max-w-7xl mx-auto h-56 w-full p-4">
    <div class="flex w-full space-x-2">
      <StyledDiv class="w-full grow">
        <template #title>
          Brainwave Stream
        </template>
      </StyledDiv>
      <StyledDiv class="max-w-96 w-full shrink-0">
        <template #title>
          Heart Rate Stream
        </template>
        <template>
          {{ data }}
        </template>
      </StyledDiv>
    </div>
    <StyledDiv>
      <template #title>
        Generated Video
      </template>
    </StyledDiv>
  </div>
</template>
<script setup lang="ts">
const { data, pending } = await useFetch("/api/terra/stress", {
  query: {
    start_date: "2025-02-15"
  }
})
</script>
