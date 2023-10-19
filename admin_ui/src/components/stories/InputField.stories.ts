import InputField from "../InputField.vue"
import "!style-loader!css-loader!less-loader!../../main.less"

export default {
    title: "Components/InputField",
    component: InputField,
    args: {
        title: "Hello",
        type: "string",
        value: "hello",
        mode: "light_mode"
    },
    argTypes: {
        type: {
            options: ["string", "number", "integer", "boolean", "array"],
            control: { type: "select" }
        },
        mode: {
            options: ["light_mode", "dark_mode"],
            control: { type: "select" }
        }
    }
}

// @ts-ignore
export const Primary = (args, { argTypes }) => {
    return {
        props: Object.keys(argTypes),
        components: { InputField },
        template: '<InputField :class="mode" v-bind="$props" v-on="$props" />',
        data: {
            mode: args.mode
        }
    }
}
