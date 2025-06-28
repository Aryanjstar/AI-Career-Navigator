import React from "react";
import styles from "./TwoColumnLayout.module.css";

interface TwoColumnLayoutProps {
    left: React.ReactNode;
    right: React.ReactNode;
}

const TwoColumnLayout: React.FC<TwoColumnLayoutProps> = ({ left, right }) => {
    return (
        <div className={styles.twoColumnRoot}>
            <div className={styles.leftColumn}>{left}</div>
            <div className={styles.rightColumn}>{right}</div>
        </div>
    );
};

export default TwoColumnLayout;

import styles from "./TwoColumnLayout.module.css";

interface TwoColumnLayoutProps {
    left: React.ReactNode;
    right: React.ReactNode;
}

const TwoColumnLayout: React.FC<TwoColumnLayoutProps> = ({ left, right }) => {
    return (
        <div className={styles.twoColumnRoot}>
            <div className={styles.leftColumn}>{left}</div>
            <div className={styles.rightColumn}>{right}</div>
        </div>
    );
};

export default TwoColumnLayout;
