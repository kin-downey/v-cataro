<template>
  <v-main>
    <v-text-field
      class="ma-4"
      outlined
      v-model="msg"
      @change="speak()"
    ></v-text-field>
    <v-btn @click="speak()">start</v-btn>
    <v-btn @click="cataro()">cataro</v-btn>
    <img
      v-if="flag"
      src="../../public/CATARO_a_1.png"
      alt="open_mouse"
      width="350"
      height="auto"
    />
    <img
      v-else
      src="../../public/CATARO_a_2.png"
      alt="close_mouse"
      width="350"
      height="auto"
    />
  </v-main>
</template>

<script>
export default {
  prop: ["key_word"],
  data() {
    return {
      count: 0,
      flag: false,
      msg: "",
      move_mouse_obj: null,
    };
  },
  methods: {
    speak() {
      console.log(this.key_word);
      const uttr = new SpeechSynthesisUtterance();
      uttr.text = this.key_word + "ですか？";
      console.log("text: ", uttr.text);
      uttr.lang = "ja";
      var move_mouse_obj = this.move_mouse();
      speechSynthesis.speak(uttr);
      // 喋り終わったら，口の動きを止める
      uttr.onend = function () {
        clearInterval(move_mouse_obj);
      };
    },
    move_mouse() {
      this.move_mouse_obj = setInterval(() => {
        this.count++;
        if (this.count % 2 == 0) {
          this.flag = true;
        } else {
          this.flag = false;
        }
      }, 500);
      return this.move_mouse_obj;
    },
  },
};
</script>
