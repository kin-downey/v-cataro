<template>
  <div>
    <v-app-bar color="#37474F">
      <v-row>
        <v-col>
          <v-toolbar-title class="mt-4 white--text"
            >研究システム</v-toolbar-title
          >
        </v-col>
        <v-col align="end" class="ma-2 mt-3">
          <UserMenu />
        </v-col>
      </v-row>
    </v-app-bar>
  </div>
</template>

<script>
import UserMenu from "@/components/UserMenu.vue";
import firebase from "@/firebase.js";
export default {
  components: {
    UserMenu,
  },
  data() {
    return {
      drawer: false,
      group: null,
    };
  },
  watch: {
    group() {
      this.drawer = false;
    },
  },
  methods: {
    createUserAccount() {
      firebase
        .auth()
        .createUserWithEmailAndPassword(this.email, this.password)
        .then(() => {
          alert("アカウントを作成しました");
          this.login_dialog = false;
          this.drawer = false;
          this.islogin = false;
        })
        .catch((error) => {
          alert("Error!", error.message);
          console.error("エラーが発生しました", error.message);
        });
    },
    logout() {
      this.show_ava = false;
      this.show_login = true;
    },
  },
};
</script>
