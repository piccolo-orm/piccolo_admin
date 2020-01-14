<template>
    <DetailViewBase>
        <AddRowForm
            :schema="schema"
            :tableName="tableName"
            v-if="schema"
        />
    </DetailViewBase>
</template>


<script lang="ts">
import Vue from "vue"
import { Location } from "vue-router"
import NavBar from "../components/NavBar.vue"
import AddRowForm from "../components/AddRowForm.vue"
import DetailViewBase from "../components/DetailViewBase.vue"

export default Vue.extend({
    props: ["tableName"],
    components: {
        AddRowForm,
        DetailViewBase
    },
    computed: {
        schema() {
            return this.$store.state.schema
        }
    },
    async mounted() {
        this.$store.commit("updateCurrentTablename", this.tableName)
        await this.$store.dispatch("fetchSchema", this.tableName)
    }
})
</script>


<style scoped lang="less">
@import "../vars.less";

div.edit_wrapper {
    margin: 0 auto;
    max-width: 40rem;
    padding: 0 0.5rem;

    a {
        text-decoration: none;
    }

    h1 {
        margin: 0;
    }

    p.referencing_title {
        color: @border_color;
        font-size: 0.8rem;
        margin-top: 1rem;
        padding: 0.5rem 0;
    }

    ul.related_tables {
        li {
            span.table {
                font-weight: bold;
                text-transform: capitalize;
            }
        }
    }
}
</style>
