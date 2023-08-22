import { Schema, OrderByConfig } from "@/interfaces"
import router from "./router"

export function readableInterval(timeRange: number) {
    if (timeRange === 0) {
        return "0 seconds"
    }

    const weeks = Math.floor(timeRange / (3600 * 24 * 7))
    const days = Math.floor((timeRange / (3600 * 24)) % 7)
    const hours = Math.floor((timeRange % (3600 * 24)) / 3600)
    const minutes = Math.floor((timeRange % 3600) / 60)
    const seconds = Math.floor(timeRange % 60)

    const weeksDisplay =
        weeks > 0 ? weeks + (weeks == 1 ? " week " : " weeks ") : ""
    const daysDisplay = days > 0 ? days + (days == 1 ? " day " : " days ") : ""
    const hoursDisplay =
        hours > 0 ? hours + (hours == 1 ? " hour " : " hours ") : ""
    const minutesDisplay =
        minutes > 0 ? minutes + (minutes == 1 ? " minute " : " minutes ") : ""
    const secondsDisplay =
        seconds > 0 ? seconds + (seconds == 1 ? " second" : " seconds") : ""
    return (
        weeksDisplay +
        daysDisplay +
        hoursDisplay +
        minutesDisplay +
        secondsDisplay
    )
}

export function titleCase(value: string) {
    return value
        .toLowerCase()
        .split(" ")
        .map(function (word) {
            return word.replace(word[0], word[0].toUpperCase())
        })
        .join(" ")
}

/**
 * We need to parse the error resposne from the server when submitting forms
 * so we can display something useful and visually pleasant to the user.
 *
 * @param error The response from the API which we need to parse.
 * @param statusCode The HTTP status code returned by the server.
 * @returns A list of error codes
 */
export function parseErrorResponse(
    error: string | { [key: string]: any },
    statusCode: number
): string[] {
    if (statusCode == 422) {
        // A validation error
        if (typeof error == "object") {
            if (error["db_error"]) {
                // Database error
                return [`Database error: ${error["db_error"]}`]
            } else if (error["detail"]) {
                // Pydantic Error
                return error["detail"].map((item: { [key: string]: any }) => {
                    // The last element is the column name
                    const fieldName = item.loc[item.loc.length - 1]
                    return `${fieldName} field - ${item.msg}`
                })
            } else if (error["custom_form_error"]) {
                // Custom form response
                return [error["custom_form_error"]]
            } else {
                return [JSON.stringify(error)]
            }
        } else {
            return [error]
        }
    } else if (statusCode == 405) {
        // Method not allowed
        if (typeof error == "object") {
            if (error["detail"]) {
                return [error["detail"]]
            } else {
                return [JSON.stringify(error)]
            }
        } else {
            return [error]
        }
    } else {
        // Something like a 500 error
        if (typeof error == "object") {
            return [JSON.stringify(error)]
        } else {
            return [error]
        }
    }
}

export function convertFormValue(params: {
    key: string
    value: any
    schema: Schema
}): any {
    let { key, value, schema } = params

    if (value == "null") {
        value = null
    } else if (schema?.properties[key].type == "array") {
        value = JSON.parse(String(value))
    } else if (schema?.properties[key].format == "uuid" && value == "") {
        value = null
    } else if (schema?.properties[key].format == "email" && value == "") {
        value = null
    } else if (schema?.properties[key].format == "date-time" && value == "") {
        value = null
    } else if (schema?.properties[key].format == "date" && value == "") {
        value = null
    } else if (schema?.properties[key].type == "integer" && value == "") {
        value = null
    } else if (schema?.properties[key].type == "number" && value == "") {
        value = null
    } else if (
        schema?.properties[key].type == "string" &&
        schema?.properties[key].nullable &&
        value == ""
    ) {
        value = null
    } else if (
        schema?.properties[key].format == "json" &&
        schema?.properties[key].nullable &&
        value == ""
    ) {
        value = null
    } else if (
        schema?.properties[key].extra.foreign_key == true &&
        value == ""
    ) {
        value = null
    }
    return value
}

/**
 * Converts the OrderByConfig array into a string which can be passed as a GET
 * parameter to PiccoloCRUD.
 */
export function getOrderByString(orderByConfigs: OrderByConfig[]): string {
    return orderByConfigs
        .map((orderByConfig) => {
            return orderByConfig.ascending
                ? orderByConfig.column
                : `-${orderByConfig.column}`
        })
        .join(",")
}

/**
 * Converts the string generated by `getOrderByString` back into an array of
 * OrderByConfig
 */
export function deserialiseOrderByString(
    orderByString: string
): OrderByConfig[] {
    return orderByString.split(",").map((subString: string) => {
        const ascending = !subString.startsWith("-")
        return {
            column: ascending ? subString : subString.slice(1),
            ascending
        } as OrderByConfig
    })
}

/**
 * Adds values as GET params to the browser's URL.
 * @param query The values to add as GET params.
 */
export const syncQueryParams = (query: { [key: string]: string }) => {
    router.replace({
        name: "rowListing",
        query
    })
}
