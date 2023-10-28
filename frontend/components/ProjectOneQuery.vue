<template>
  <div class="w-full h-screen p-8 pt-14 m-0 flex justify-space-evenly">
    <div>
      <v-form class="max-w-2xl bg-teal-500 rounded-2xl p-5 drop-shadow-lg">
        <p class="text-4xl text-center text-white font-sans font-semibold pb-5">
          Ask a question for a specific project
        </p>
        <v-text-field v-model="query" variant="solo" label="Query"/>
        <v-text-field v-model="projectID" variant="solo" label="Project ID"/>

        <v-btn @click="buttonClick">Submit Job</v-btn>
      </v-form>
    </div>
    <!-- <div>{{ query }}</div> -->

    <ModelOutput :text_data="val"/>
  </div>
</template>

<script setup>
let val = ref("");
let projectID = ref("");
let query = ref("");

  const lorem =
      'Based on the provided information, the project "Umbrella Programme for Preparation of National Communications and Biennial Update Reports to the UNFCCC" involves 25 countries.';

async function buttonClick() {
  val.value = lorem;
}
</script>

<style scoped lang="scss"></style>
