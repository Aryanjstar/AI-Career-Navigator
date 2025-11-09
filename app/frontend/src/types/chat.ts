export enum ChatHistoryLoadingState {
    Loading = "loading",
    Success = "success",
    Error = "error"
}

export interface Conversation {
    id: string;
    title: string;
    messages: any[];
    timestamp: number;
}

export enum DialogType {
    None = "none",
    History = "history",
    Settings = "settings"
}

export interface Answers {
    [key: string]: any;
}
