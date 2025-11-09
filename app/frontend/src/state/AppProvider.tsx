import React, { createContext, useContext, ReactNode } from "react";

interface AppState {
    feedbackEnabled: boolean;
    chatHistoryEnabled: boolean;
    isCosmosDBAvailable: {
        cosmosDB: boolean;
    };
    frontendSettings: {
        feedback_enabled: boolean;
    };
}

interface AppStateContextType {
    state: AppState;
}

const defaultState: AppState = {
    feedbackEnabled: false,
    chatHistoryEnabled: false,
    isCosmosDBAvailable: {
        cosmosDB: false
    },
    frontendSettings: {
        feedback_enabled: false
    }
};

export const AppStateContext = createContext<AppStateContextType | undefined>(undefined);

interface AppProviderProps {
    children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
    return <AppStateContext.Provider value={{ state: defaultState }}>{children}</AppStateContext.Provider>;
};

export const useAppState = () => {
    const context = useContext(AppStateContext);
    if (context === undefined) {
        throw new Error("useAppState must be used within an AppProvider");
    }
    return context;
};
