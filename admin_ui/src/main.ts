import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

/******************************************************************************
 Font Awesome */

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faAngleDown,
  faAngleLeft,
  faAngleRight,
  faAngleUp,
  faBars,
  faEdit,
  faExternalLinkAlt,
  faFilter,
  faHome,
  faInfoCircle,
  faMoon,
  faPlus,
  faSignOutAlt,
  faSort,
  faSun,
  faTable,
  faTimes,
  faTools,
  faTrashAlt,
  faUser,
} from '@fortawesome/free-solid-svg-icons';
library.add(
  faAngleDown,
  faAngleLeft,
  faAngleRight,
  faAngleUp,
  faBars,
  faEdit,
  faExternalLinkAlt,
  faFilter,
  faHome,
  faInfoCircle,
  faMoon,
  faPlus,
  faSignOutAlt,
  faSort,
  faSun,
  faTable,
  faTimes,
  faTools,
  faTrashAlt,
  faUser,
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
