<template>
<div id="filter_overlay">
    <div class="modal">
        <p class="close">
            <a
                href="#"
                v-on:click.prevent="$emit('close')">Close</a>
        </p>
        <h1>Filter</h1>

        <form v-on:submit.prevent="submitForm($event)">
            <div
                v-for="field in schema.properties"
                v-bind:key="field.title">

                <label>{{ field.title }}</label>
                <input
                    type="number"
                    v-bind:name="field.title.toLowerCase()"
                    v-if="field.type == 'integer'" />
                <input
                    type="text"
                    v-bind:name="field.title.toLowerCase()"
                    v-if="field.type == 'string'" />
                <input
                    type="checkbox"
                    v-bind:name="property.title.toLowerCase()"
                    v-if="property.type == 'boolean'" />
            </div>
            <button>Apply</button>
            <button>Clear filters</button>
        </form>
    </div>
</div>
</template>


<script lang="ts">
export default {
    computed: {
        schema: function() {
            return this.$store.state.schema
        },
        tableName: function() {
            return this.$store.state.currentTableName
        }
    },
    methods: {
        submitForm: async function(event) {
            var form = new FormData(event.target)

            var json = {}
            for (var i of form.entries()) {
                json[i[0]] = i[1]
            }
            await this.$store.dispatch(
                'fetchRows',
                {
                    tableName: this.tableName,
                    params: json
                }
            )
            this.$emit('close')
        }
    }
}
</script>


<style scoped lang="less">
div#filter_overlay {
    position: absolute;
    top: 0%;
    left: 0%;
    height: 100%;
    width: 100%;
    background-color: rgba(0,0,0,0.7);

    div.modal {
        background-color: #2d2d2d;
        width: 30rem;
        margin: 1rem auto;
        box-sizing: border-box;
        padding: 1rem;
        border-radius: 0.5rem;

        label, input {
            width: 100%;
            display: block;
        }

        p.close {
            text-align: right;
        }
    }
}
</style>
