import React from "react";

interface SpinnerProps {
    size?: "small" | "medium" | "large";
    className?: string;
}

export const Spinner: React.FC<SpinnerProps> = ({ size = "medium", className = "" }) => {
    const sizeClasses = {
        small: "w-4 h-4",
        medium: "w-8 h-8",
        large: "w-12 h-12"
    };

    return <div className={`animate-spin rounded-full border-2 border-primary-200 border-t-primary-600 ${sizeClasses[size]} ${className}`}></div>;
};

export default Spinner;
