import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import RowListing from './views/RowListing.vue'
import EditRow from './views/EditRow.vue'
import Login from './views/Login.vue'


Vue.use(Router);


export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
        },
        {
            path: '/login/',
            name: 'login',
            component: Login,
        },
        {
            path: '/:tableName/',
            name: 'rowListing',
            component: RowListing,
            props: true
        },
        {
            path: '/:tableName/:rowID/',
            name: 'editRow',
            component: EditRow,
            props: true
        },
    ],
});
