<template class="">
  <div class="">
    <v-app class="">
      <router-view class="" />
      <v-bottom-navigation>
        <v-btn to="/" nuxt> Question </v-btn>
        <v-btn to="/question" nuxt>Question</v-btn>
        <v-btn to="/spreadsheet" nuxt>Spreadsheet</v-btn>
        <v-btn to="/jobs" nuxt> Jobs </v-btn>
      </v-bottom-navigation>
    </v-app>
  </div>
</template>
<script setup lang="ts"></script>
