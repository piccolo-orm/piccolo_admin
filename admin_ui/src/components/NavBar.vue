<template>
    <div id="nav">
        <span id="burger_menu">
            <a
                href="#"
                v-on:click.prevent="showSidebar = showSidebar ? false : true"
            >
                <font-awesome-icon icon="bars" v-if="!showSidebar" />
                <font-awesome-icon icon="times" v-else />
            </a>
        </span>

        <h1>
            <router-link to="/">
                <font-awesome-icon icon="tools" />
                {{ siteName }}
            </router-link>
        </h1>

        <ul>
            <li style="margin-right: 1rem">
                <a
                    href="#"
                    title="Translations"
                    v-on:click.prevent="
                        showLanguageDropdown = !showLanguageDropdown
                    "
                    ><font-awesome-icon icon="language" size="lg"
                /></a>
                <NavTranslationsMenu
                    v-if="showLanguageDropdown"
                    @closeDropdown="closeDropdown"
                />
            </li>
            <li>
                <a
                    href="#"
                    id="user"
                    data-uitest="nav_dropdown_button"
                    :title="username"
                    v-on:click.prevent="showDropdown = !showDropdown"
                >
                    <font-awesome-icon icon="user" />
                    {{ truncatedUsername }}
                    <font-awesome-icon icon="angle-up" v-if="showDropdown" />
                    <font-awesome-icon icon="angle-down" v-if="!showDropdown" />

                    <NavDropDownMenu v-show="showDropdown" />
                </a>
            </li>
        </ul>
    </div>

    <SidebarOverlay v-if="showSidebar" />
</template>

<script lang="ts">
import { defineComponent } from "vue"
import NavDropDownMenu from "./NavDropDownMenu.vue"
import SidebarOverlay from "./SidebarOverlay.vue"
import NavTranslationsMenu from "./NavTranslationsMenu.vue"

export default defineComponent({
    props: {
        username: {
            type: String,
            default: "Unknown"
        },
        siteName: {
            type: String,
            default: "Piccolo Admin"
        }
    },
    data() {
        return {
            showSidebar: false,
            showDropdown: false,
            showLanguageDropdown: false
        }
    },
    computed: {
        truncatedUsername() {
            const username = this.username
            if (username.length > 20) {
                return username.slice(0, 16) + "..."
            } else {
                return username
            }
        }
    },
    components: {
        SidebarOverlay,
        NavDropDownMenu,
        NavTranslationsMenu
    },
    methods: {
        closeDropdown() {
            this.showLanguageDropdown = false
        }
    }
})
</script>

<style lang="less">
@import "../vars.less";

#nav {
    background-color: darken(@dark_grey, 5%);
    border-bottom: 1px solid @border_color;
    box-sizing: border-box;
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
            display: none;
        }
    }

    ul {
        padding: 0;
        flex-grow: 0;
        text-align: right;

        @media (max-width: @mobile_width) {
            flex-grow: 1;
        }

        li {
            display: inline-block;
            position: relative;
        }
    }

    a {
        color: white;
        font-weight: bold;
        text-decoration: none;
    }
}
</style>
