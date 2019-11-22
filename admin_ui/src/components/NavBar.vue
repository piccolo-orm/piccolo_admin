<template>
    <div id="nav">
        <router-link to="/">
            <h1>
                <font-awesome-icon icon="tools" />Piccolo Admin
            </h1>
        </router-link>
        <p>
            <a
                href="#"
                style="padding-right: 1rem;"
            >
                <font-awesome-icon icon="user" />admin
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
</template>


<script lang="ts">
import Vue from "vue"
import axios from "axios"


export default Vue.extend({
    computed: {
        tableName() {
            return this.$store.state.currentTableName
        }
    },
    methods: {
        async logout() {
            if (window.confirm("Are you sure you want to logout?")) {
                console.log("Logging out")
                try {
                    await axios.post('./logout/')
                } catch(error) {
                    console.log('Logout failed')
                    console.log(error.response)
                }

            }
        }
    }
})
</script>


<style lang="less">
#nav {
    background-color: rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 0 0.5rem;

    h1 {
        padding-right: 2rem;
        margin: 0;
        font-size: 1.2rem;
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
        flex-grow: 1;
        text-align: right;
    }

    a {
        font-weight: bold;
        text-decoration: none;
    }
}
</style>
