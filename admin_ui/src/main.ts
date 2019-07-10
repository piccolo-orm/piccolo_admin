import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

/******************************************************************************
 Font Awesome */

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faPlus,
  faFilter,
  faEdit,
  faTrashAlt,
  faUser,
  faHome,
  faTable,
  faTools,
  faSignOutAlt,
  faAngleDown
} from '@fortawesome/free-solid-svg-icons';
library.add(
  faPlus,
  faFilter,
  faEdit,
  faTrashAlt,
  faUser,
  faHome,
  faTable,
  faTools,
  faSignOutAlt,
  faAngleDown
);
Vue.component('font-awesome-icon', FontAwesomeIcon);

/*****************************************************************************/

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App)
}).$mount('#app');
