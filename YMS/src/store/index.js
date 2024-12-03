import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    assignedEquipments: [], // 할당된 장비 목록
  },
  mutations: {
    // 장비 할당 데이터를 추가
    ADD_EQUIPMENT(state, equipment) {
      const exists = state.assignedEquipments.find(
        (item) => item.id === equipment.id
      );
      if (!exists) {
        state.assignedEquipments.push(equipment);
      }
    },
    // 모든 할당된 장비를 초기화
    CLEAR_EQUIPMENTS(state) {
      state.assignedEquipments = [];
    },
  },
  actions: {
    // Action to add equipment
    addEquipment({ commit }, equipment) {
      commit("ADD_EQUIPMENT", equipment);
    },
    // Action to clear all equipments
    clearEquipments({ commit }) {
      commit("CLEAR_EQUIPMENTS");
    },
  },
  getters: {
    // 할당된 장비 목록 가져오기
    assignedEquipments: (state) => state.assignedEquipments,
  },
});
