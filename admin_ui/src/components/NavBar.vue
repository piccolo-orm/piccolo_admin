<template>
<div id="nav">
    <h1><font-awesome-icon icon="tools" /> Piccolo Admin</h1>
    <p>
        <a href="#" v-on:click.prevent="logout" style="padding-right: 1rem;">
            <font-awesome-icon icon="user" /> admin <font-awesome-icon icon="angle-down" />
        </a>

        <a href="#" v-on:click.prevent="logout">
            Log out <font-awesome-icon icon="sign-out-alt" />
        </a>
    </p>
</div>
</template>


<script lang="ts">
import Vue from 'vue'


export default Vue.extend({
    computed: {
        tableName() {
            return this.$store.state.currentTableName
        }
    },
    methods: {
        logout() {
            window.confirm('Are you sure you want to logout?')
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

        &.router-link-exact-active {
            color: #42b983;
        }
    }
}
</style>
