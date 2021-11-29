const mutations = {
    setAxios(state, axios) {
      console.log("[mutations] set axios");
      state.axios = axios;
    },
  };
  export default mutations;