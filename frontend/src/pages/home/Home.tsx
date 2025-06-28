import React from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Home.module.css";

const features = [
    { key: "resume", title: "Resume Analysis", description: "Upload your resume and get instant feedback." },
    { key: "skillgap", title: "Skill Gap Analysis", description: "Identify gaps in your skills and get recommendations." },
    { key: "interview", title: "Interview Prep", description: "Practice interview questions and get tips." },
    { key: "chat", title: "Career Chat", description: "Get personalized career guidance and AI-powered answers to your questions." }
];

const featureRoutes = {
    resume: "/resume-analysis",
    skillgap: "/skill-gap",
    interview: "/interview-prep",
    chat: "/chat"
};

const Home: React.FC = () => {
    const navigate = useNavigate();
    return (
        <div className={styles.homeRoot}>
            <h1 className={styles.homeTitle}>AI Career Navigator</h1>
            <div className={styles.cardGrid}>
                {features.map(f => (
                    <div key={f.key} className={styles.featureCard} onClick={() => navigate(featureRoutes[f.key as keyof typeof featureRoutes])}>
                        <div className={styles.featureTitle}>{f.title}</div>
                        <div className={styles.featureDescription}>{f.description}</div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Home;

import { useNavigate } from "react-router-dom";
import styles from "./Home.module.css";

const features = [
    { key: "resume", title: "Resume Analysis", description: "Upload your resume and get instant feedback." },
    { key: "skillgap", title: "Skill Gap Analysis", description: "Identify gaps in your skills and get recommendations." },
    { key: "interview", title: "Interview Prep", description: "Practice interview questions and get tips." },
    { key: "chat", title: "Career Chat", description: "Get personalized career guidance and AI-powered answers to your questions." }
];

const featureRoutes = {
    resume: "/resume-analysis",
    skillgap: "/skill-gap",
    interview: "/interview-prep",
    chat: "/chat"
};

const Home: React.FC = () => {
    const navigate = useNavigate();
    return (
        <div className={styles.homeRoot}>
            <h1 className={styles.homeTitle}>AI Career Navigator</h1>
            <div className={styles.cardGrid}>
                {features.map(f => (
                    <div key={f.key} className={styles.featureCard} onClick={() => navigate(featureRoutes[f.key as keyof typeof featureRoutes])}>
                        <div className={styles.featureTitle}>{f.title}</div>
                        <div className={styles.featureDescription}>{f.description}</div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Home;
