<template>
  <v-main>
    <v-btn outlined @click="test()">test</v-btn>
  </v-main>
</template>

<script>
import kuromoji from "kuromoji";
export default {
  data() {
    return {};
  },
  methods: {
    analysis() {
      const text = "親譲りの無鉄砲で小供の時から損ばかりしている";
      kuromoji.builder({ dicPath: "/dict" }).build((err, tokenizer) => {
        if (err) {
          console.log(err);
        } else {
          const tokens = tokenizer.tokenize(text);
          console.log(tokens);
        }
      });
    },
  },
};
</script>
