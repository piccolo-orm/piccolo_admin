<template>
    <div>
        <ul
            class="table_list"
            v-bind:key="index"
            v-for="(tableName, index) in tableNames"
        >
            <p v-if="index != 'null'" class="group">
                <font-awesome-icon icon="layer-group" />
                <span>{{ index }}</span>
            </p>
            <li v-bind:key="name" v-for="name in tableName">
                <router-link
                    :to="{ name: 'rowListing', params: { tableName: name } }"
                    class="subtle"
                    v-bind:class="{ active: isActive(name) }"
                >
                    <font-awesome-icon icon="level-up-alt" />
                    <span>{{ name | readable }}</span>
                </router-link>
            </li>
        </ul>
    </div>
</template>


<script lang="ts">
import Vue from "vue"

export default Vue.extend({
    computed: {
        tableNames() {
            return this.$store.state.tableNames
        },
        currentTableName() {
            return this.$store.state.currentTableName
        }
    },
    methods: {
        showListing(tableName: string) {
            this.$store.commit("updateCurrentTablename", tableName)
            this.$router.push({ name: "rowListing", params: { tableName } })
        },
        isActive(tableName: string): boolean {
            return this.currentTableName === tableName
        }
    },
    filters: {
        readable(value) {
            return value.split("_").join(" ")
        }
    },
    async mounted() {
        await this.$store.dispatch("fetchTableNames")
    }
})
</script>

<style scoped lang="less">
.group {
    cursor: auto;

    span {
        font-weight: bold;
    }
}
</style>
