<template>
    <div class="timedelta_widget">
        <div class="segment">
            <p>{{ $t("Weeks") }}</p>
            <select v-model.number="weeks" v-on:change="emitEvent" id="weeks">
                <option :key="'w' + week" v-for="week in weekRange">
                    {{ week }}
                </option>
            </select>
        </div>

        <div class="segment">
            <p>{{ $t("Days") }}</p>
            <select v-model.number="days" v-on:change="emitEvent" id="days">
                <option :key="'d' + day" v-for="day in dayRange">
                    {{ day }}
                </option>
            </select>
        </div>

        <div class="segment">
            <p>{{ $t("Hours") }}</p>
            <select v-model.number="hours" v-on:change="emitEvent" id="hours">
                <option :key="'h' + hour" v-for="hour in hourRange">
                    {{ hour }}
                </option>
            </select>
        </div>

        <div class="segment">
            <p>{{ $t("Minutes") }}</p>
            <select
                v-model.number="minutes"
                v-on:change="emitEvent"
                id="minutes"
            >
                <option :key="'m' + minute" v-for="minute in minuteRange">
                    {{ minute }}
                </option>
            </select>
        </div>

        <div class="segment">
            <p>{{ $t("Seconds") }}</p>
            <select
                v-model.number="seconds"
                v-on:change="emitEvent"
                id="seconds"
            >
                <option :key="'s' + second" v-for="second in secondRange">
                    {{ second }}
                </option>
            </select>
        </div>
    </div>
</template>

<script lang="ts">
const MINUTE = 60
const HOUR = MINUTE * 60
const DAY = HOUR * 24
const WEEK = DAY * 7
let selectSeconds: any = 0
let selectMinutes: any = 0
let selectHours: any = 0
let selectDays: any = 0
let selectWeeks: any = 0

export default {
    props: {
        timedelta: {
            // In seconds
            default: 0,
            type: Number
        }
    },
    data() {
        return {
            weekRange: [...Array(500).keys()],
            dayRange: [...Array(7).keys()],
            hourRange: [...Array(24).keys()],
            minuteRange: [...Array(60).keys()],
            secondRange: [...Array(60).keys()],
            weeks: 0,
            days: 0,
            hours: 0,
            minutes: 0,
            seconds: 0
        }
    },
    methods: {
        emitEvent() {
            const timedelta =
                this.seconds +
                this.minutes * MINUTE +
                this.hours * HOUR +
                this.days * DAY +
                this.weeks * WEEK
            this.$emit("newTimedelta", timedelta)

            let s = document.getElementById("seconds") as HTMLSelectElement
            selectSeconds = s.options[s.options.selectedIndex].value

            let m = document.getElementById("minutes") as HTMLSelectElement
            selectMinutes = m.options[m.options.selectedIndex].value

            let h = document.getElementById("hours") as HTMLSelectElement
            selectHours = h.options[h.options.selectedIndex].value

            let d = document.getElementById("days") as HTMLSelectElement
            selectDays = d.options[d.options.selectedIndex].value

            let w = document.getElementById("weeks") as HTMLSelectElement
            selectWeeks = w.options[w.options.selectedIndex].value
        },
        setupValues(timedelta) {
            this.weeks = Math.floor(timedelta / WEEK)
            timedelta += -this.weeks * WEEK

            this.days = Math.floor(timedelta / DAY)
            timedelta += -this.days * DAY

            this.hours = Math.floor(timedelta / HOUR)
            timedelta += -this.hours * HOUR

            this.minutes = Math.floor(timedelta / MINUTE)
            timedelta += -this.minutes * MINUTE

            this.seconds = timedelta
        }
    },
    watch: {
        timedelta(timedelta) {
            this.setupValues(timedelta)
        }
    },
    mounted() {
        this.seconds = parseInt(selectSeconds) || 0
        this.minutes = parseInt(selectMinutes) || 0
        this.hours = parseInt(selectHours) || 0
        this.days = parseInt(selectDays) || 0
        this.weeks = parseInt(selectWeeks) || 0
    }
}
</script>


<style lang="less" scoped>
div.timedelta_widget {
    display: flex;
    flex-direction: row;

    div.segment {
        padding-right: 0.4rem;
        width: 100%;

        &:last-child {
            padding-right: 0;
        }

        p {
            text-transform: uppercase;
            font-size: 0.6rem;
            line-height: 1;
            margin: 0;
            padding: 0.3rem 0;
        }
    }
}
</style>