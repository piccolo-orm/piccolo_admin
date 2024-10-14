<template>
    <div>
        <ul class="table_list">
            <li v-for="form in formGroups.ungrouped" v-bind:key="form">
                <router-link
                    :to="{ name: 'addForm', params: { formSlug: form.slug } }"
                    class="subtle"
                    ><font-awesome-icon icon="level-up-alt" class="rotated90" />
                    <span>{{ form.name }}</span></router-link
                >
            </li>

            <template v-for="(formNames, groupName) in formGroups.grouped">
                <li class="group">
                    <a
                        href="#"
                        class="subtle"
                        @click.prevent="toggleGroup(String(groupName))"
                        title="Click to toggle children."
                    >
                        <font-awesome-icon icon="layer-group" />
                        <span class="name">{{ groupName }}</span>
                        <span
                            class="ellipsis"
                            v-if="hiddenGroups.indexOf(String(groupName)) != -1"
                            >...</span
                        >
                    </a>
                </li>

                <template v-if="hiddenGroups.indexOf(String(groupName)) == -1">
                    <li v-for="form in formNames" v-bind:key="form">
                        <router-link
                            :to="{
                                name: 'addForm',
                                params: { formSlug: form.slug }
                            }"
                            class="subtle"
                            ><font-awesome-icon
                                icon="level-up-alt"
                                class="rotated90"
                            />
                            <span>{{ form.name }}</span></router-link
                        >
                    </li>
                </template>
            </template>
        </ul>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
    data() {
        return {
            hiddenGroups: [] as string[]
        }
    },
    computed: {
        formGroups() {
            return this.$store.state.formGroups
        }
    },
    methods: {
        toggleGroup(groupName: string) {
            const hiddenGroups: string[] = this.hiddenGroups
            const index = hiddenGroups.indexOf(groupName)
            if (index == -1) {
                hiddenGroups.push(groupName)
            } else {
                hiddenGroups.splice(index, 1)
            }
            this.hiddenGroups = hiddenGroups
        }
    },
    async mounted() {
        await this.$store.dispatch("fetchFormConfigs")
        await this.$store.dispatch("fetchFormGroups")
    }
})
</script>

<style scoped lang="less">
li.group {
    font-size: 0.7em;

    a {
        text-transform: uppercase;

        span {
            &.name {
                padding-left: 0;
            }

            &.ellipsis {
                flex-grow: 1;
                text-align: right;
            }
        }
    }
}
</style>
