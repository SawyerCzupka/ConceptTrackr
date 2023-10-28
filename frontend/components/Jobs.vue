<template>
  <div class="bg-teal-600 h-screen w-screen">
    <p>{{ jobs.jobs }}</p>
    <v-btn @click="jobs.add_task()">PushMe</v-btn>
  </div>
</template>

<script setup lang="ts">

import {useJobsStore} from "~/composables/jobs";

const jobs = useJobsStore()

</script>
