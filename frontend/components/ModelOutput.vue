<template>
  <div class="text-lg rounded-2xl p-5 bg-gray-200 text-black max-w-4xl">
    <p class="text-center text-2xl font-bold">Model Output</p>
    <hr class="h-px my-5 bg-black border-0 dark:bg-gray-700" />
    <p>{{ props.text_data }}</p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  text_data: {
    type: String,
    required: true,
  },
});
</script>
