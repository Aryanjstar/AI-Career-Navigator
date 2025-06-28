import React from "react";
import styles from "./FullScreenAnswer.module.css";

interface FullScreenAnswerProps {
    answer: React.ReactNode;
    onClose: () => void;
    backToHome?: boolean; // Optional prop for navigation
}

const FullScreenAnswer: React.FC<FullScreenAnswerProps> = ({ answer, onClose }) => {
    return (
        <div className={styles.fullScreenRoot}>
            <button className={styles.closeButton} onClick={onClose} aria-label="Close">
                &larr; Back
            </button>
            <div className={styles.answerContent}>{answer}</div>
        </div>
    );
};

export default FullScreenAnswer;

import styles from "./FullScreenAnswer.module.css";

interface FullScreenAnswerProps {
    answer: React.ReactNode;
    onClose: () => void;
    backToHome?: boolean; // Optional prop for navigation
}

const FullScreenAnswer: React.FC<FullScreenAnswerProps> = ({ answer, onClose }) => {
    return (
        <div className={styles.fullScreenRoot}>
            <button className={styles.closeButton} onClick={onClose} aria-label="Close">
                &larr; Back
            </button>
            <div className={styles.answerContent}>{answer}</div>
        </div>
    );
};

export default FullScreenAnswer;
