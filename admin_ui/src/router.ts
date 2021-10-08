import { RouteRecordRaw, createRouter, createWebHashHistory } from "vue-router";

import AddRow from './views/AddRow.vue'
import EditRow from './views/EditRow.vue'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import RowListing from './views/RowListing.vue'
import AddForm from './views/AddForm.vue'



const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'home',
        component: Home,
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/forms/:formSlug/',
        name: 'addForm',
        component: AddForm,
        props: true
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
]

const router = createRouter({
    routes,
    history: createWebHashHistory()
});

export default router;


