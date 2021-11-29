const actions = {
post_memo_list({ state }, { param }) {
    return new Promise((resolve, reject) => {
      state.axios
        .get(
          `/income/months/graph/?school_id=${state.schoolId}&fiscalyear=${param.fiscalyear}&grade_num=${param.grade}`,
          {
            headers: {
              Authorization: "Bearer " + state.keycloak.token,
            },
          }
        )
        .then((response) => {
          // commit("setReceiptChartData", response.data);
          resolve(response.data);
        }).catch((e) => {
            console.log("Error occurred in API");
            console.log(e);
            reject(e);
          });
      });
    },
};
export default actions;