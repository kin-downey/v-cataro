<template>
  <v-main>
    <v-spacer></v-spacer>
    <v-menu v-if="islogin">
      <template v-slot:activator="{ on, attrs }">
        <v-btn small fab color="green" v-bind="attrs" v-on="on">
          <v-avatar size="40" color="green">
            <img src="../assets/Unknown.jpeg" alt="pomodoro" />
          </v-avatar>
        </v-btn>
      </template>
      <v-list>
        <v-list-item>
          <v-btn text color="red" @click="logout()">logout</v-btn>
        </v-list-item>
      </v-list>
    </v-menu>

    <v-dialog v-else v-model="login_dialog" width="500">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          class="mt-2 mx-4"
          small
          text
          color="white"
          v-bind="attrs"
          v-on="on"
        >
          <v-icon>mdi-login</v-icon>login</v-btn
        >
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2"> ログイン </v-card-title>

        <v-divider></v-divider>

        <v-text-field
          v-model="email"
          class="mx-4"
          label="メールアドレス"
          clearable
        ></v-text-field>
        <v-text-field
          class="mx-4"
          v-model="password"
          :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules.required, rules.min]"
          :type="show1 ? 'text' : 'password'"
          name="input-10-1"
          label="パスワード"
          hint="最低8文字以上"
          counter
          @click:append="show1 = !show1"
        ></v-text-field>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="createUserAccount()">signup</v-btn>
          <v-btn color="primary" text @click="login()"> login </v-btn>
          <v-btn color="red" text @click="login_dialog = false"> close </v-btn>
        </v-card-actions>
        <v-card-text class="caption"
          >アカウントをお持ちでない方は<br />任意のメールアドレス，パスワードを入力して
          SIGNUP を押してください</v-card-text
        >
      </v-card>
    </v-dialog>
  </v-main>
</template>

<script>
import firebase from "@/firebase.js";
export default {
  data() {
    return {
      islogin: false,
      login_dialog: false,
      email: "",
      password: "",
      show1: false,
      rules: {
        required: (value) => !!value || "Required.",
        min: (v) => v.length >= 6 || "Min 6 characters",
        emailMatch: () => "The email and password you entered don't match",
      },
    };
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
    login() {
      firebase
        .auth()
        .signInWithEmailAndPassword(this.email, this.password)
        .then(() => {
          this.islogin = true;
        })
        .catch((error) => {
          alert("アカウントが存在しません", error.message);
          console.log(error);
        });
    },
    logout() {
      firebase
        .auth()
        .signOut()
        .then(() => {
          this.islogin = false;
        })
        .catch((error) => {
          console.log(`ログアウト時にエラーが発生しました (${error})`);
        });
    },
  },
};
</script>
