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
  faAngleDown,
  faSort,
  faBars
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
  faAngleDown,
  faSort,
  faBars
);
Vue.component('font-awesome-icon', FontAwesomeIcon);

/*****************************************************************************/

import axios from 'axios';
import Cookies from 'js-cookie';

// Add the CSRF token
axios.interceptors.request.use(function (config) {
  if (['POST', 'PUT', 'DELETE'].indexOf(config.method.toUpperCase()) != -1) {
    const csrfToken = Cookies.get('csrftoken');
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

/*****************************************************************************/

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App)
}).$mount('#app');
