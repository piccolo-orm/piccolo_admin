<template>
    <div class="sidebar">
        <p class="opaque">
            <router-link class="subtle" to="/">
                <font-awesome-icon icon="home" />Home
            </router-link>
        </p>
        <p class="opaque">
            <font-awesome-icon icon="table" />Tables
            <span style="float: right">
                <font-awesome-icon icon="angle-down" />
            </span>
        </p>
        <TableNav />
        <p class="opaque" v-show="formConfigs.length > 0">
            <font-awesome-icon icon="cogs" />Forms
            <span style="float: right">
                <font-awesome-icon icon="angle-down" />
            </span>
        </p>
        <FormNav />
    </div>
</template>

<script>
import Vue from "vue"
import TableNav from "./TableNav.vue"
import FormNav from "./FormNav.vue"

export default Vue.extend({
    components: {
        TableNav,
        FormNav,
    },
    computed: {
        formConfigs() {
            return this.$store.state.formConfigs
        },
    },
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
                border-left: 3px solid rgba(0, 0, 0, 0);

                &:hover {
                    background-color: rgba(0, 0, 0, 0.2);
                }

                &.active {
                    border-left: 3px solid @light_blue;
                }
            }
        }
    }
}
</style>