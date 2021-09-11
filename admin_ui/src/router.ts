import Vue from 'vue';
import Router from 'vue-router';

import AddRow from './views/AddRow.vue'
import EditRow from './views/EditRow.vue'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import RowListing from './views/RowListing.vue'
import AddForm from './views/AddForm.vue'


Vue.use(Router);


export default new Router({
    mode: 'hash',
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
            path: '/:tableName/add/',
            name: 'addRow',
            component: AddRow,
            props: true
        },
        {
            path: '/:tableName/:rowID/',
            name: 'editRow',
            component: EditRow,
            props: true
        },
        {
            path: '/forms/:formName/schema/',
            name: 'addForm',
            component: AddForm,
            props: true
        },
    ],
});
