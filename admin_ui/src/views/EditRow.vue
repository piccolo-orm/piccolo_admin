<template>
<div>
    <NavBar />
    <div class="edit_wrapper">
        <p>
            <a href='#' v-on:click.prevent="$router.go(-1)">Back</a>
        </p>

        <h1>Edit</h1>

        <form>
            <div v-for="property in schema.properties" v-bind:key="property.title">
                <label>{{ property.title }}</label>
                <input type="text" v-bind:value="getValue(property.title)">
            </div>
            <button>Save</button>
        </form>
    </div>
</div>
</template>


<script>
import Vue from 'vue'
import NavBar from '../components/NavBar.vue'


export default Vue.extend({
    props: [
        'tableName',
        'rowID'
    ],
    components: {
        NavBar,
    },
    computed: {
        schema() {
            return this.$store.state.schema
        },
        selectedRow() {
            // The form should be reusable???
            return this.$store.state.selectedRow
        }
    },
    methods: {
        getValue(value) {
            return this.selectedRow ? this.selectedRow[value.toLowerCase()] : ''
        }
    },
    async mounted() {
        this.$store.commit('updateCurrentTablename', this.tableName)
        await Promise.all([
            this.$store.dispatch(
                'fetchSingleRow',
                {
                    tableName: this.tableName,
                    rowID: this.rowID
                }
            ),
            this.$store.dispatch('fetchSchema', this.tableName)
        ])
    }
})
</script>


<style lang="less">
div.edit_wrapper {
    margin: 0 auto;
    max-width: 40rem;
    padding: 0 0.5rem;

    h1 {
        margin: 0;
    }
}
</style>
