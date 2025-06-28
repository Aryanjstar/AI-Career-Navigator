import { AskRequest, AskResponse } from "../types/ask";

export const askApi = async (request: AskRequest): Promise<AskResponse> => {
    // Mock implementation for now
    return {
        answer: "This is a mock response",
        thoughts: "Mock thoughts",
        data_points: [],
        context: {}
    };
};

export default askApi;
