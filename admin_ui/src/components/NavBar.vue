<template>
    <div>
        <div id="nav">
            <span id="burger_menu">
                <a
                    href="#"
                    v-on:click.prevent="showSidebar = showSidebar ? false : true"
                >
                    <font-awesome-icon icon="bars" />
                </a>
            </span>

            <h1>
                <router-link to="/">
                    <font-awesome-icon icon="tools" />Piccolo Admin
                </router-link>
            </h1>

            <ul>
                <li>
                    <a
                        href="#"
                        id="user"
                        v-on:click.prevent="showDropdown = !showDropdown"
                    >
                        <font-awesome-icon icon="user" />
                        {{ username }}
                        <font-awesome-icon
                            icon="angle-up"
                            v-if="showDropdown"
                        />
                        <font-awesome-icon
                            icon="angle-down"
                            v-if="!showDropdown"
                        />
                        <DropDownMenu v-if="showDropdown" />
                    </a>
                </li>
            </ul>
        </div>

        <SidebarOverlay v-if="showSidebar" />
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import DropDownMenu from "./DropDownMenu.vue"
import SidebarOverlay from "./SidebarOverlay.vue"

export default Vue.extend({
    data() {
        return {
            showSidebar: false,
            showDropdown: false
        }
    },
    computed: {
        tableName() {
            return this.$store.state.currentTableName
        },
        username() {
            let user = this.$store.state.user
            return user ? user.username : "Unknown"
        }
    },
    components: {
        SidebarOverlay,
        DropDownMenu
    }
})
</script>


<style lang="less">
@import "../vars.less";

#nav {
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 0 0.5rem;

    span#burger_menu {
        @media (min-width: @mobile_width) {
            display: none;
        }
    }

    h1 {
        color: white;
        flex-grow: 1;
        padding: 1rem 0;
        margin: 0;
        font-size: 1.2rem;

        @media (max-width: @mobile_width) {
            text-align: center;
        }
    }

    ul {
        padding: 0;
        flex-grow: 0;
        text-align: right;

        li {
            display: inline-block;
            position: relative;
        }
    }

    a#user {
        padding-right: 1rem;
    }

    a {
        color: white;
        font-weight: bold;
        text-decoration: none;
    }
}
</style>
