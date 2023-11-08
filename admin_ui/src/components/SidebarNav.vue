<template>
    <div class="sidebar">
        <p class="opaque">
            <router-link class="subtle" to="/">
                <font-awesome-icon icon="home" />{{ $t("Home") }}
            </router-link>
        </p>
        <p class="opaque" v-on:click="isHiddenTables = !isHiddenTables">
            <font-awesome-icon icon="table" />{{ $t("Tables") }}
            <span style="float: right">
                <font-awesome-icon
                    icon="angle-down"
                    title="Show tables"
                    v-if="isHiddenTables"
                />
                <font-awesome-icon icon="angle-up" title="Hide tables" v-else />
            </span>
        </p>
        <TableNav v-show="!isHiddenTables" />
        <p
            class="opaque"
            v-if="formConfigs.length > 0"
            v-on:click="isHiddenForms = !isHiddenForms"
        >
            <font-awesome-icon icon="cogs" />{{ $t("Forms") }}
            <span style="float: right">
                <font-awesome-icon
                    icon="angle-down"
                    title="Show forms"
                    v-if="isHiddenForms"
                />
                <font-awesome-icon icon="angle-up" title="Hide forms" v-else />
            </span>
        </p>
        <FormNav v-show="!isHiddenForms" />
        <p
            class="opaque"
            v-if="Object.keys(customLinks).length > 0"
            v-on:click="isHiddenLinks = !isHiddenLinks"
        >
            <font-awesome-icon icon="link" />{{ $t("Links") }}
            <span style="float: right">
                <font-awesome-icon
                    icon="angle-down"
                    title="Show links"
                    v-if="isHiddenLinks"
                />
                <font-awesome-icon icon="angle-up" title="Hide links" v-else />
            </span>
        </p>
        <LinksNav v-show="!isHiddenLinks" />
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import TableNav from "./TableNav.vue"
import FormNav from "./FormNav.vue"
import LinksNav from "./LinksNav.vue"

export default defineComponent({
    data() {
        return {
            isHiddenTables: false,
            isHiddenForms: false,
            isHiddenLinks: false
        }
    },
    components: {
        TableNav,
        FormNav,
        LinksNav
    },
    computed: {
        formConfigs() {
            return this.$store.state.formConfigs
        },
        customLinks() {
            return this.$store.state.customLinks
        }
    }
})
</script>

<style lang="less">
@import "../vars.less";

div.sidebar {
    background-color: rgba(0, 0, 0, 0.1);
    overflow-y: auto;
    height: 100%;

    p {
        padding: 0.5rem;
        margin: 0;
        cursor: pointer;
        user-select: none;

        a {
            display: block;
            text-decoration: none;
        }
    }

    ul {
        margin: 0;
        padding: 0;

        li {
            list-style: none;
            text-transform: capitalize;

            a {
                align-items: center;
                display: flex;
                padding: 0.5rem;
                text-decoration: none;
                border-left: 3px solid rgba(0, 0, 0, 0);

                &:hover {
                    background-color: rgba(0, 0, 0, 0.2);
                }

                &.active {
                    border-left: 3px solid @light_blue;
                }

                span {
                    display: block;
                    box-sizing: border-box;
                    padding: 0 0.5rem;
                    user-select: none;
                }
            }
        }
    }
}
</style>
