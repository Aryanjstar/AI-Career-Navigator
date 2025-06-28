export interface AskRequest {
    question: string;
    approach: string;
    context?: any;
}

export interface AskResponse {
    answer: string;
    thoughts?: string;
    data_points?: string[];
    context?: any;
}

export interface Citation {
    content: string;
    id: string;
    title?: string;
    filepath?: string;
    url?: string;
    metadata?: any;
}
