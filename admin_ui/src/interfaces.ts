export interface CreateRow {
    tableName: string
    data: object
}

export interface DeleteRow {
    tableName: string
    rowID: number
}

export interface UpdateRow {
    tableName: string
    rowID: number
    data: object
}

export interface FetchRowsConfig {
    tableName: string
    params: object
}


export interface FetchSingleRowConfig {
    tableName: string
    rowID: number
}

export interface APIResponseMessage {
    contents: string
    type: string
}
