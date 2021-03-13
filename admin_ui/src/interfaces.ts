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


export interface FetchIdsConfig {
    tableName: string
    limit: number
    search: string
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

export interface SortByConfig {
    property: string
    ascending: boolean
}

export interface RowCountAPIResponse {
    count: number
    page_size: number
}


export interface TableReference {
    tableName: string
    columnName: string
}


export interface TableReferencesAPIResponse {
    references: TableReference[]
}
