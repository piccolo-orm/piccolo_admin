<template>
    <div class="sidebar">
        <p class="opaque">
            <router-link to="/">
                <font-awesome-icon icon="home" />Home
            </router-link>
        </p>
        <p class="opaque">
            <font-awesome-icon icon="table" />Tables
            <span style="float: right;">
                <font-awesome-icon icon="angle-down" />
            </span>
        </p>
        <TableNav />
    </div>
</template>

<script>
import Vue from "vue"
import TableNav from "./TableNav.vue"

export default Vue.extend({
    components: {
        TableNav
    }
})
</script>

<style lang="less">
@import "../vars.less";

div.sidebar {
    background-color: rgba(0, 0, 0, 0.1);
    height: 100%;

    p {
        padding: 0.5rem;
        margin: 0;

        a {
            text-decoration: none;
        }
    }

    ul {
        margin: 0;

        li {
            a {
                display: block;
                padding: 0.5rem;
                text-decoration: none;

                &:hover {
                    background-color: rgba(0, 0, 0, 0.2);
                }

                &.active {
                    border-right: 3px solid @light_blue;
                }
            }
        }
    }
}
</style>