<template>
    <table>
        <thead>
            <slot name="thead"></slot>
        </thead>

        <tbody>
            <slot name="tbody"></slot>
        </tbody>
    </table>
</template>

<script>
export default {}
</script>

<style scoped lang="less">
@import "../vars.less";

table {
    border-collapse: collapse;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: -1px 0px 2px 1px rgba(0, 0, 0, 0.1);
    width: 100%;

    tr {
        text-align: left;

        span.boolean {
            padding-left: 0.5rem;

            svg.correct {
                color: @green;
            }
            svg.incorrect {
                color: @red;
            }
        }
    }
    td {
        font-size: 0.9em;
    }
    th {
        font-size: 0.7em;
        text-transform: uppercase;

        &:last-child {
            text-align: right;
        }
    }
    td,
    th {
        padding: 0.7rem;
    }
    td {
        &.last-child {
            text-align: right;
            width: auto;
        }

        a {
            text-decoration: none;

            &.delete:hover {
                color: @red;
            }
        }

        ul {
            padding: 0;
            text-align: right;
            min-width: 4rem;

            li {
                display: inline-block;
                margin-left: 0.5rem;
            }
        }
    }
}
</style>
