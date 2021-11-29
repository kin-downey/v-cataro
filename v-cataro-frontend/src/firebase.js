// import firebase from "firebase";
// import "firebase/auth";
// import "firebase/firestore";

// const config = {
//   apiKey: "AIzaSyDV8JDkpGMWuNV0WrlcQOKX_WC6Q5cCt7g",
//   authDomain: "v-cataro.firebaseapp.com",
//   projectId: "v-cataro",
//   storageBucket: "v-cataro.appspot.com",
//   messagingSenderId: "598729592808",
//   appId: "1:598729592808:web:ccc741140cce79e2a2de5d",
//   measurementId: "G-0E8V6TB8B8",
// };

// firebase.initializeApp(config);

// firebase.getCurrentUser = () => {
//   return new Promise((resolve, reject) => {
//     const unsubscribe = firebase.auth().onAuthStateChanged((user) => {
//       unsubscribe();
//       resolve(user);
//     }, reject);
//   });
// };

// const settings = { timestampsInSnapshots: true };
// firebase.firestore().settings(settings);

// export default firebase;
