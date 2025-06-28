import React from "react";

interface AnswerErrorProps {
    error: Error | unknown;
    onRetry?: () => void;
}

export const AnswerError: React.FC<AnswerErrorProps> = ({ error, onRetry }) => {
    const errorMessage = error instanceof Error ? error.message : "An unexpected error occurred";

    return (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center">
                <div className="flex-shrink-0">
                    <span className="text-red-500">⚠️</span>
                </div>
                <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">Error</h3>
                    <div className="mt-2 text-sm text-red-700">
                        <p>{errorMessage}</p>
                    </div>
                    {onRetry && (
                        <div className="mt-4">
                            <button type="button" onClick={onRetry} className="bg-red-100 text-red-800 px-3 py-1 rounded text-sm hover:bg-red-200">
                                Try Again
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AnswerError;
