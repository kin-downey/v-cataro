<template>
  <v-app>
    <v-main>
      <v-row>
        <v-col align="end">
          <img
            v-if="flag"
            src="../../public/CATARO_a_1.png"
            alt="open_mouse"
            width="450"
            height="auto"
          />
          <img
            v-else
            src="../../public/CATARO_a_2.png"
            alt="close_mouse"
            width="450"
            height="auto"
          />
        </v-col>
        <v-col align="center" class="mt-8">
          <div>
            <p>neutral: {{ neutral }}</p>
            <p>happy: {{ happy }}</p>
            <p>angry: {{ angry }}</p>
            <p>sad: {{ sad }}</p>
            <p>surprised: {{ surprised }}</p>
            <p>fearful: {{ fearful }}</p>
            <p>disgusted: {{ disgusted }}</p>
          </div>
        </v-col>
      </v-row>
      <v-row align="center" class="ma-2">
        <v-col align="center">
          <v-btn @click="up_pitch()">pitch up</v-btn>
          <v-btn @click="down_pitch()">pitch down</v-btn>
          <v-btn @click="up_rate()">rate up</v-btn>
          <v-btn @click="down_rate()">rate down</v-btn>
          <v-btn @click="test_speech()">test speech</v-btn>
        </v-col>
        <v-col class="mx-4">
          <h3>{{ this.pitch_message }}</h3>
          <h4>{{ this.pitch }}</h4>
          <h3>{{ this.rate_message }}</h3>
          <h4>{{ this.rate }}</h4>
        </v-col>
        <v-col>
          <video
            ref="video"
            id="video"
            width="300"
            height="300"
            playsinline
            muted
            autoplay
          ></video>
          <canvas ref="canvas" id="myCanvas" width="1" height="1"></canvas>
        </v-col>
      </v-row>
      <div v-if="show_button">
        <v-row align="center">
          <v-col align="center">
            <v-btn color="primary" @click="onclick()"> スタート </v-btn>
          </v-col>
        </v-row>
      </div>
      <div v-else>
        <v-row align="center">
          <v-col align="center">
            <h3>対話が開始されました</h3>
            <h4>対話開始まで10秒ほどかかる場合があります．</h4>
          </v-col>
        </v-row>
      </div>
      <v-row class="mt-5">
        <v-col align="center">
          <p>{{ text }}</p>
        </v-col>
      </v-row>
    </v-main>
  </v-app>
</template>

<script>
// import firebase from "../firebase.js";
import * as faceapi from "face-api.js";
import kuromoji from "kuromoji";
import axios from "axios";
//import * as canvas from 'canvas';

export default {
  name: "voice",
  data() {
    return {
      show_button: true,
      user_email: "",
      word: "",
      text: "",
      angry: "",
      disgusted: "",
      fearful: "",
      happy: "",
      neutral: "",
      sad: "",
      surprised: "",
      timestamp: "",
      changed_id: "",
      timer: null,
      canvas: null,
      video: null,
      recognition: null,
      key_word: "",
      count: 0,
      flag: false,
      msg: "",
      move_mouse_obj: null,
      user_name: "こんにちは。。",
      aiduti_obj: null,
      recog_flag: 0,
      response: "",
      rate: 0.8,
      pitch: 1,
      pitch_message: "pitch",
      pitch_min: 0,
      pitch_max: 2,
      rate_message: "rate",
      rate_min: 0.5,
      rate_max: 10,
      emotion: "",
      subject: "",
    };
  },
  mounted() {
    //PCのフロントカメラを起動し、リアルタイムの映像をvideoタグに表示する
    this.video = document.getElementById("video");
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ audio: false, video: true })
        .then((stream) => {
          this.video.srcObject = stream;
        });
    }

    this.canvas = this.$refs.canvas;
  },

  methods: {
    test_speech() {
      const uttr = new SpeechSynthesisUtterance();
      uttr.text = "マイクテスト．マイクテスト";
      this.rate = 0.65;
      this.pitch = 0.6;
      uttr.lang = "ja";
      uttr.pitch = this.pitch;
      uttr.rate = this.rate;
      console.log("test: ", uttr.pitch);
      speechSynthesis.speak(uttr);
    },
    onclick() {
      this.show_button = false;
      // this.set_email();
      this.init_recognition();
    },
    async init_recognition() {
      this.recognition = new window.webkitSpeechRecognition();

      this.recognition.lang = "ja-JP";
      this.recognition.interimResults = true;
      this.recognition.continuous = true;
      this.recognition.onend = function () {
        console.log("voice is ended");
      };
      await faceapi.loadSsdMobilenetv1Model("/models");
      await faceapi.loadFaceExpressionModel("/models");
      this.face_recog();
      console.log("complete");
      const text = "こんにちは，今日は鶏を食べました．";
      console.log(text);
      kuromoji.builder({ dicPath: "/dict" }).build((err, tokenizer) => {
        if (err) {
          console.log(err);
        } else {
          const tokens = tokenizer.tokenize(text);
          for (let token of tokens) {
            if (token.pos == "名詞") {
              console.log("token: ", token.basic_form);
              // const key_word = token.basic_form;
            }
          }
        }
        this.aiduti();
        this.start_recognition();
      });
    },
    start_recognition() {
      this.recognition.onresult = (event) => {
        for (let i = event.resultIndex; i < event.results.length; i++) {
          let transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            //finalTranscript += transcript;
            this.text = transcript;
            this.recognition.stop();
            this.face_recog();
            this.analysis(this.text);
          }
        }
      };
      this.recognition.start();
    },
    // 応答生成までの間に返す相槌（表情によって変化させる）
    quick_response(key_word) {
      const _this = this;
      axios
        .post("http://localhost:8090/hello/emotion", {
          key_word: key_word,
          neutral: this.neutral,
          happy: this.happy,
          sad: this.sad,
          angry: this.angry,
          fearful: this.fearful,
          disgusted: this.disgusted,
          surprised: this.surprised,
        })
        .then(function (response) {
          _this.response = response.data.sentence;
          _this.emotion = response.data.emotion;
          if (_this.emotion == "sad") {
            _this.pitch = 0.65;
            _this.subject = response.data.subject;
          } else if (_this.emotion == "angry") {
            _this.pitch = 0.7;
            _this.subject = response.data.subject;
          } else if (_this.emotion == "happy") {
            _this.pitch = 1.8;
          }

          console.log(response.data.sentence);
          _this.speak(_this.response);
        });
    },
    async face_recog() {
      const detectionWithExpressions = await faceapi
        .detectSingleFace(this.video)
        .withFaceExpressions();

      this.neutral = detectionWithExpressions.expressions.neutral;
      this.happy = detectionWithExpressions.expressions.happy;
      this.sad = detectionWithExpressions.expressions.sad;
      this.angry = detectionWithExpressions.expressions.angry;
      this.fearful = detectionWithExpressions.expressions.fearful;
      this.disgusted = detectionWithExpressions.expressions.disgusted;
      this.surprised = detectionWithExpressions.expressions.surprised;

      clearInterval(this.aiduti_obj);
    },
    api_post(key_words) {
      let _this = this;
      axios
        .post("http://localhost:8090/hello/answer ", {
          word: key_words,
        })
        .then(function (response) {
          if (_this.emotion == "sad") {
            _this.speak(_this.subject);
          } else if (_this.emotion == "angry") {
            _this.speak(_this.subject);
          } else {
            console.log(response.data.sentence);
            _this.speak(response.data.sentence);
            console.log(response.data);
            _this.word = "";
          }
        });
    },
    // 単語を形態素解析する
    async analysis(input_text) {
      const text = input_text;
      var key_words = [];
      kuromoji.builder({ dicPath: "/dict" }).build((err, tokenizer) => {
        if (err) {
          console.log(err);
        } else {
          const tokens = tokenizer.tokenize(text);
          for (let token of tokens) {
            if (token.pos == "名詞") {
              console.log("token: ", token.basic_form);
              key_words.push(token.basic_form);
              this.key_word = token.basic_form;
            }
          }
          console.log("for key_word: ", key_words);
          this.api_post(key_words);
          this.quick_response(this.key_word);
        }
      });
    },
    aiduti() {
      const uttr = new SpeechSynthesisUtterance();
      var move_mouse_obj = this.move_mouse();
      uttr.text = "こんにちは。昨日の夜ご飯に何を食べましたか？";
      uttr.lang = "ja";
      uttr.pitch = this.pitch;
      uttr.rate = this.rate;
      speechSynthesis.speak(uttr);
      uttr.onend = function () {
        clearInterval(move_mouse_obj);
      };
    },
    async speak(key_word) {
      const uttr = new SpeechSynthesisUtterance();
      var move_mouse_obj = this.move_mouse();
      uttr.text = key_word;
      uttr.lang = "ja";
      // ピッチとレートを設定
      uttr.pitch = this.pitch;
      uttr.rate = this.rate;
      speechSynthesis.speak(uttr);
      this.user_name = "";
      const recognition = this.recognition;
      // 喋り終わったら，口の動きを止める
      uttr.onend = function () {
        clearInterval(move_mouse_obj);
        recognition.start();
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
    up_pitch() {
      if (this.pitch > 1.9) {
        this.pitch_message = "すでにピッチは最大値です．";
      } else {
        this.pitch += 0.1;
      }
    },
    down_pitch() {
      if (this.pitch < 0.1) {
        this.pitch_message = "すでにピッチは最小です";
      } else {
        this.pitch_message = "";
        this.pitch -= 0.1;
      }
    },
    up_rate() {
      this.rate += 0.1;
    },
    down_rate() {
      this.rate -= 0.1;
    },
  },
};
</script>
<style>
.overlay {
  position: absolute;
}
</style>
