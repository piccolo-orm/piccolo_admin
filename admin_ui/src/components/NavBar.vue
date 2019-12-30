<template>
    <div>
        <div id="nav">
            <span
                id="burger_menu"
                v-on:click.prevent="showSidebar = showSidebar ? false : true"
            >
                <font-awesome-icon icon="bars" />
            </span>

            <h1>
                <router-link to="/">
                    <font-awesome-icon icon="tools" />Piccolo Admin
                </router-link>
            </h1>

            <p>
                <a
                    href="#"
                    id="user"
                >
                    <font-awesome-icon icon="user" />
                    {{ username }}
                </a>

                <a
                    href="#"
                    v-on:click.prevent="logout"
                >
                    Log out
                    <font-awesome-icon icon="sign-out-alt" />
                </a>
            </p>
        </div>

        <SidebarOverlay v-if="showSidebar" />
    </div>
</template>


<script lang="ts">
import Vue from "vue"
import axios from "axios"
import SidebarOverlay from "./SidebarOverlay.vue"

export default Vue.extend({
    data() {
        return {
            showSidebar: false
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
        SidebarOverlay
    },
    methods: {
        async logout() {
            if (window.confirm("Are you sure you want to logout?")) {
                console.log("Logging out")
                try {
                    await axios.post("./api/logout/")
                    this.$router.push({ name: "login" })
                } catch (error) {
                    console.log("Logout failed")
                    console.log(error)
                }
            }
        }
    }
})
</script>


<style lang="less">
@import "../vars.less";

#nav {
    background-color: rgba(0, 0, 0, 0.2);
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

        li {
            display: inline-block;
            text-transform: uppercase;
            font-size: 0.8em;

            &:not(:first-child) {
                &:before {
                    content: ">";
                    padding: 0 0.5rem;
                }
            }

            a {
                text-decoration: none;

                &:hover {
                    text-decoration: underline;
                }
            }
        }
    }

    p {
        flex-grow: 0;
        text-align: right;
    }

    a#user {
        padding-right: 1rem;

        @media (max-width: @mobile_width) {
            display: none;
        }
    }

    a {
        font-weight: bold;
        text-decoration: none;
    }
}
</style>
