<template>
  <v-main>
    <v-text-field
      class="ma-4"
      outlined
      v-model="msg"
      @change="speak()"
    ></v-text-field>
  </v-main>
</template>
<script>
export default {
  data() {
    return {
      msg: "",
    };
  },
  methods: {
    speak() {
      const uttr = new SpeechSynthesisUtterance();

      let voices = speechSynthesis.getVoices();
      console.log("voices: ", voices);
      uttr.text = this.msg;
      uttr.lang = "ja";
      speechSynthesis.speak(uttr);
    },
  },
};
</script>
