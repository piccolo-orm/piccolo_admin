<template>
    <div class="sidebar">
        <p>
            <router-link to="/">
                <font-awesome-icon icon="home" />Home
            </router-link>
        </p>
        <p>
            <font-awesome-icon icon="table" />Tables
        </p>
        <TableNav />
    </div>
</template>

<script>
import TableNav from "./TableNav.vue"

export default {
    components: {
        TableNav
    }
}
</script>

<style lang="less">
@import "../vars.less";

div.sidebar {
    border-right: 1px solid @border_color;
    width: 15rem;

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
                background-color: rgba(0, 0, 0, 0.2);
                display: block;
                padding: 0.5rem;
                text-decoration: none;

                &:hover {
                    background-color: rgba(0, 0, 0, 0.4);
                }

                &.active {
                    border-right: 3px solid @light_blue;
                }
            }
        }
    }
}
</style>