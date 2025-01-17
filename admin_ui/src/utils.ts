import {
    type Schema,
    type OrderByConfig,
    getType,
    isNullable
} from "@/interfaces"
import router from "./router"
import moment from "moment"

/*****************************************************************************/
// Filters

/**
 * Converts an identifier like `my_column` to `my column`.
 * @param value The string to convert.
 * @returns A readable version of a string
 */
export function readable(value: string) {
    return value.split("_").join(" ")
}

/**
 * We need to parse ISO 8601 duration string (e.g. P17DT14706S) to
 * seconds and then convert to human readable interval.
 *
 * @param timeValue ISO 8601 duration string which we need to parse.
 * @returns A string of nicelly formated timeValue
 */
export function readableInterval(timeValue: string) {
    const parsedTimeValue = moment.duration(timeValue)
    const timeRange = parsedTimeValue.asSeconds()
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

/**
 * We need to convert interval from seconds to ISO 8601 duration
 * string (e.g. P17DT14706S) for form fields.
 *
 * @param value interval seconds which we need to convert.
 * @returns ISO 8601 duration string
 */
export function secondsToISO8601Duration(value: number) {
    return moment.duration(value, "seconds").toISOString()
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
        return null
    }

    const property = schema.properties[key]

    const nullable = property.extra?.nullable

    if (nullable == true && value == "") {
        return null
    }

    // For Piccolo custom forms, there is no `extra` attribute, instead we
    // have to look at the OpenAPI schema:
    if (nullable == undefined && isNullable(property) && value == "") {
        return null
    }

    if (getType(property) == "array") {
        value = JSON.parse(String(value))
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
export const syncQueryParams = (
    tableName: string,
    query: { [key: string]: string }
) => {
    router.replace({
        name: "rowListing",
        params: { tableName },
        query
    })
}
