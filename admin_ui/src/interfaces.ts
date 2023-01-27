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
    offset?: number
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

/*****************************************************************************/
// Translations
export interface TranslationListItemAPI {
    language_name: string
    language_code: string
}

export interface TranslationsListAPIResponse {
    translations: TranslationListItemAPI[]
    default_language_code: string
}

export interface TranslationAPIResponse {
    language_name: string
    language_code: string
    translations: { [key: string]: string }
}

/*****************************************************************************/
// File storage

export interface StoreFileAPIResponse {
    file_key: string
}

export interface MediaViewerConfig {
    fileKey: string
    columnName: string
    tableName: string
}

/*****************************************************************************/

export interface Choice {
    display_name: string
    value: string
}

export interface Choices {
    [key: string]: Choice
}

/*****************************************************************************/

export interface Schema {
    title: string
    type: string
    properties: Properties
    help_text: null
    visible_column_names: string[]
    visible_filter_names: string[]
    rich_text_columns: string[]
    media_columns: string[]
    visible_fields_options: string[]
    primary_key_name: string
    link_column_name: string
}

export interface Properties {
    [key: string]: RowConfig
}

export interface RowConfig {
    title: string
    default?: any
    extra: RowConfigExtra
    nullable: boolean
    type: string
    format?: string
    maxLength?: number
    items?: ArrayItems
}

export interface RowConfigExtra {
    help_text: null | string
    choices: Choices | null
    foreign_key?: boolean
    to?: string
}

export interface ArrayItems {
    type: string
}

export interface FormConfig {
    name: string
    slug: string
    description: string
}
