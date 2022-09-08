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

export function parseErrorResponse(error: Object) {
    let errorsArray: string[] = []

    const databaseError = error["db_error"]
    const validationError = error["detail"]

    if (databaseError) {
        errorsArray.push(databaseError)
    } else {
        validationError.forEach((item: any) => {
            errorsArray.push(
                `Field ${item.loc[1]} - ${item.msg}`
            )
        })
    }
    return errorsArray
}
