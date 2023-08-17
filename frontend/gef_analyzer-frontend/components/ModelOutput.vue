<template>
  <div class="text-lg rounded-3xl p-4 bg-black max-w-4xl">
    <p>{{ props.text_data }}</p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps(["text_data"]);
</script>
