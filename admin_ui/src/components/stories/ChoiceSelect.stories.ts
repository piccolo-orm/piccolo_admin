import ChoiceSelect from "../ChoiceSelect.vue"
import "../../main.less"

export default {
    title: "Components/ChoiceSelect",
    component: ChoiceSelect,
    args: {
        value: "medium",
        fieldName: "shirt_size",
        choices: {
            small: { display_name: "Small", value: "s" },
            medium: { display_name: "Medium", value: "m" },
            large: { display_name: "Large", value: "l" }
        },
        isFilter: true,
        isNullable: true,
        mode: "light_mode"
    },
    argTypes: {
        mode: {
            options: ["light_mode", "dark_mode"],
            control: { type: "select" }
        }
    }
}

// @ts-ignore
export const Primary = (args, { argTypes }) => {
    return {
        components: { ChoiceSelect },
        props: Object.keys(argTypes),
        template:
            '<ChoiceSelect :class="mode" v-bind="$props" v-on="$props" />',
        data: {
            model: args.mode
        }
    }
}
