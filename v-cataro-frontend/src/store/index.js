import Vue from 'vue'
import Vuex from 'vuex'
// import createPersistedState from "vuex-persistedstate";
import state from './state.js'
import mutations from './mutations.js'
import actions from './actions.js'
import getters from './getters.js'
Vue.use(Vuex)
const store = new Vuex.Store({
    state: state,
    mutations: mutations,
    actions: actions,
    getters: getters,
    // plugins: [createPersistedState({paths: ['receiptData', 'chartData'], storage: window.sessionStorage})]
})
export default store