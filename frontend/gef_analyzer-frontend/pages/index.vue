<template>
  <div class="bg-gray-200">
    <section class="">
      <div class="flex align-middle justify-center">
        <ProjectOneQuery />
        <v-btn @click="click">Download CSV</v-btn>
      </div>
    </section>
  </div>
</template>

<script setup>
import ProjectOneQuery from "~/components/ProjectOneQuery.vue";

const { download_csv } = useDownload();

async function click() {
  console.log("Clicked");
  await download_csv();
}

// import axios from "axios";
//
// async function download_csv_pages() {
//   try {
//     const response = await axios.get("/api/download");
//     const blob = new Blob([response.data], { type: "text/csv" });
//     const url = URL.createObjectURL(blob);
//
//     const link = document.createElement("a");
//     link.href = url;
//     link.download = "exported_data.csv";
//     link.click();
//     URL.revokeObjectURL(url);
//   } catch (error) {
//     console.error("An error occurred:", error);
//   }
// }
</script>
