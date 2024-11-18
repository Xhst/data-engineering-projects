 export interface PaperDto {
    filename: string;
    Title: string;
    Authors: string | null;
    Keywords: string | null;
    Abstract: string | null;
    score: number;
}

export interface PaperSearchDto {
    documents: PaperDto[];
    suggestion: string | null;
    queryTimeMs: number;
}

// Type guard for PaperSearchDto
export function isPaperSearchDto(data: any): data is PaperSearchDto {
    return data.documents?.length > 0 
        && "Title" in data.documents[0]
        && "Authors" in data.documents[0]
        && "Keywords" in data.documents[0]
        && "Abstract" in data.documents[0];
}

export interface TableDto {
    paperId: string;
    tableId: string;
    score: number;
}

export interface TableSearchDto {
    tables: TableDto[];
    suggestion: string | null;
    queryTimeMs: number;
}

// Type guard for TableSearchDto
export function isTableSearchDto(data: any): data is TableSearchDto {
    return data.tables?.length > 0 
        && "paperId" in data.tables[0]
        && "tableId" in data.tables[0];
}