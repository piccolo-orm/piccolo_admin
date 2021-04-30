<template>
    <div class="sidebar">
        <p class="opaque">
            <router-link
                class="subtle"
                :class="{ active: isActive('home') }"
                to="/"
            >
                <font-awesome-icon icon="home" />Home
            </router-link>
        </p>
        <p class="opaque">
            <router-link
                class="subtle"
                :class="{ active: isActive('userManagement') }"
                to="/user-management"
            >
                <font-awesome-icon icon="user" /> Users
            </router-link>
        </p>
        <p class="opaque header">
            <font-awesome-icon icon="table" />Tables
            <span style="float: right">
                <font-awesome-icon icon="angle-down" />
            </span>
        </p>
        <div class="table_nav_wrapper">
            <TableNav />
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue"
import TableNav from "./TableNav.vue"

export default Vue.extend({
    components: {
        TableNav,
    },
    methods: {
        isActive(routeName: string) {
            return this.$route.name == routeName
        },
    },
})
</script>

<style lang="less">
@import "../vars.less";

.activeLink() {
    border-left: 3px solid @light_blue;
}

div.sidebar {
    background-color: rgba(0, 0, 0, 0.1);
    height: 100%;

    p {
        margin: 0;

        a {
            border-left: 3px solid rgba(0, 0, 0, 0);
            display: block;
            padding: 0.5rem;
            text-decoration: none;

            &.active {
                .activeLink();
            }
        }

        &.header {
            border-left: 3px solid rgba(0, 0, 0, 0);
            padding: 0.5rem;
        }
    }

    div.table_nav_wrapper {
        ul {
            margin: 0;

            li {
                a {
                    display: block;
                    padding: 0.5rem;
                    text-decoration: none;
                    border-left: 3px solid rgba(0, 0, 0, 0);

                    &.active {
                        .activeLink();
                    }

                    &:hover {
                        background-color: rgba(0, 0, 0, 0.2);
                    }
                }
            }
        }
    }
}
</style>