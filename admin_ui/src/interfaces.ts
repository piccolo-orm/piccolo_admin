export interface CreateRow {
    tableName: string
    data: object
}

export type RowID = number | string

export interface DeleteRow {
    tableName: string
    rowID: RowID
}

export interface UpdateRow {
    tableName: string
    rowID: RowID
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
    rowID: RowID
}

export interface APIResponseMessage {
    contents: string
    type: "success" | "error" | "neutral"
}

export interface OrderByConfig {
    column: string | null
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

export interface SchemaExtra {
    help_text: string | null
    link_column_name: string
    media_columns: string[]
    order_by: OrderByConfig[]
    primary_key_name: string
    rich_text_columns: string[]
    visible_column_names: string[]
    visible_fields_options: string[]
    visible_filter_names: string[]
    time_resolution: { [key: string]: number }
}

export interface Schema {
    extra: SchemaExtra
    properties: Properties
    required: string[]
    title: string
    type: string
}

export interface Properties {
    [key: string]: Property
}

export interface AnyOf {
    type: string
    maxLength?: number
    format?: string
    // If the element is an array:
    items?: {
        format: string
        type: string
    }
}

export interface Property {
    title: string
    default?: any
    extra: PropertyExtra
    type?: string
    anyOf?: AnyOf[]
    format?: string
    maxLength?: number
}

export interface ForeignKey {
    to: string
    target_column: string
}

// These are additional values we add to the JSON schema.
export interface PropertyExtra {
    choices: Choices | null
    foreign_key?: ForeignKey
    help_text: string | null
    nullable: boolean
    secret: boolean
    unique: boolean
    widget?: string
}

export interface FormConfig {
    name: string
    slug: string
    description: string
}

/*****************************************************************************/

export const getType = (property: Property): string => {
    // We know that one of these will be true:
    return (property.type || property.anyOf?.[0].type) as string
}

// Determines if the property is nullable based off the OpenAPI type.
export const isNullable = (property: Property): boolean => {
    return (property.anyOf ?? []).filter((i) => i.type == "null").length > 0
}

export const getFormat = (property: Property): string | undefined => {
    if (property.format) {
        return property.format
    }

    const anyOfItem = property.anyOf?.[0]

    if (anyOfItem) {
        if (anyOfItem.type == "array") {
            return anyOfItem.items?.format
        } else {
            return anyOfItem.format
        }
    }
}
