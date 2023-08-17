<template>
  <div class="w-full p-8 pt-14 m-0 flex justify-space-evenly">
    <v-form class="max-w-2xl">
      <p
        class="text-4xl text-center text-white font-sans font-semibold underline underline-offset-auto pb-5"
      >
        Ask a question for a specific project
      </p>
      <v-text-field variant="solo" label="Query" />
      <v-text-field variant="solo" label="Project ID" />

      <v-btn type="">Submit</v-btn>
    </v-form>

    <ModelOutput :text_data="lorem" />
  </div>
</template>

<script setup>
const lorem =
  "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vestibulum\n" +
  "      iaculis magna, vel lacinia ligula pretium nec. Vivamus enim lorem,\n" +
  "      suscipit in nulla vitae, imperdiet vulputate mi. Phasellus ac pharetra ex.\n" +
  "      Aliquam eu bibendum arcu, nec mattis elit. Fusce cursus non erat id\n" +
  "      mollis. Fusce a ex placerat, accumsan elit faucibus, pretium nibh. Duis\n" +
  "      iaculis vitae lorem consectetur blandit. Nullam nec sem ante. Vestibulum\n" +
  "      commodo, massa vitae cursus dapibus, nulla neque commodo nunc, at feugiat\n" +
  "      lorem eros eu lorem. In in magna eget ligula pulvinar vehicula. Sed mollis\n" +
  "      sapien nibh, a dictum felis rutrum in. Phasellus tortor leo, blandit non\n" +
  "      sapien vitae, consequat efficitur nibh. Fusce nec nibh semper, gravida ex\n" +
  "      consequat, semper risus. Suspendisse ut justo bibendum ex commodo\n" +
  "      vehicula. Nam sit amet suscipit mi, non feugiat dolor. Mauris lacinia\n" +
  "      porta pulvinar. Fusce placerat eleifend sapien, eu mattis metus. In\n" +
  "      vulputate semper dolor ut cursus. Aliquam non dapibus lacus. Sed ut\n" +
  "      elementum nunc. Integer porta, lacus a ultrices interdum, enim mauris\n" +
  "      venenatis enim, lobortis dignissim mi turpis vel neque. Aliquam congue\n" +
  "      quam vitae lectus suscipit, ac elementum ex facilisis. Integer ipsum\n" +
  "      lectus, ultrices cursus efficitur in, pretium in dolor. Nunc gravida odio\n" +
  "      a purus luctus scelerisque. Cras diam sem, mattis eget facilisis sit amet,\n" +
  "      interdum at neque. Vivamus consectetur felis nunc, vel consequat quam\n" +
  "      condimentum in. In auctor augue et eleifend egestas. Donec et scelerisque\n" +
  "      mauris. Aenean tempor, enim id mattis sagittis, diam orci accumsan metus,\n" +
  "      sit amet efficitur nunc arcu id dui. Cras porttitor eget justo id\n" +
  "      vehicula. Sed vel purus felis. Sed neque orci, volutpat eget malesuada\n" +
  "      eget, sagittis eget lorem. Nulla neque nibh, lobortis at lorem eu,\n" +
  "      scelerisque aliquet orci. In iaculis auctor urna, quis bibendum magna.\n" +
  "      Curabitur aliquet congue varius. Donec risus orci, posuere vitae erat a,\n" +
  "      aliquet egestas diam. Maecenas bibendum enim in orci ultrices, vulputate\n" +
  "      commodo urna imperdiet. Suspendisse risus mi, malesuada et scelerisque\n" +
  "      vel, hendrerit sed nulla. Aliquam erat volutpat. Aenean eget feugiat ex.\n" +
  "      In hac habitasse platea dictumst. Interdum et malesuada fames ac ante\n" +
  "      ipsum primis in faucibus. Quisque nulla nisi, finibus sagittis rutrum ut,\n" +
  "      finibus sed magna. Vivamus nunc ante, tincidunt ut molestie eu, ultricies\n" +
  "      at ante. Aliquam erat volutpat. Quisque sollicitudin leo non ornare\n" +
  "      sagittis. Phasellus tincidunt ornare libero, sed interdum justo semper\n" +
  "      vel. Donec finibus lectus sem, tristique consectetur mi sagittis eget.\n" +
  "      Etiam sit amet odio non ante congue mollis. Morbi nec aliquet nulla. Proin\n" +
  "      consequat dictum felis, id finibus mauris rhoncus id. Quisque viverra erat\n" +
  "      sed cursus egestas. Etiam eget fringilla tortor. Etiam pulvinar faucibus\n" +
  "      risus, sed fermentum ipsum feugiat ac. Nam semper, ipsum vitae consectetur\n" +
  "      feugiat, massa elit imperdiet odio, in maximus tortor turpis a enim.\n" +
  "      Maecenas sit amet sem vitae nisi tempus fringilla in eu lorem. Cras purus\n" +
  "      ligula, euismod in sodales eget, luctus sit amet diam. Vestibulum\n" +
  "      ullamcorper suscipit sapien vitae eleifend. Cras accumsan lacus ac\n" +
  "      convallis accumsan. Curabitur mattis convallis leo nec sagittis.";
</script>

<style scoped lang="scss"></style>
