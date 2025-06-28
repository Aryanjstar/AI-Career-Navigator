import React, { useRef, useState, useEffect } from "react";
import { AskRequest, AskResponse } from "../../types/ask";
import { Approach } from "../../types/approaches";
import { askApi } from "../../services/askApi";
import { Spinner } from "../../components/Spinner";
import { Answer } from "../../components/Answer";
import { AnswerError } from "../../components/AnswerError";
import { AnalysisPanel } from "../../components/AnalysisPanel";
import { AnalysisPanelTabs } from "../../components/AnalysisPanel/AnalysisPanelTabs";
import { SettingsButton } from "../../components/SettingsButton";
import { QuestionInput } from "../../components/QuestionInput";
import styles from "./OneShot.module.css";
import TwoColumnLayout from "../../components/layout/TwoColumnLayout";
import FullScreenAnswer from "../../components/FullScreenAnswer";

export default function OneShot() {
    const lastQuestionRef = useRef<string>("");
    const chatMessageStreamEnd = useRef<HTMLDivElement | null>(null);

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [isStreaming, setIsStreaming] = useState<boolean>(false);
    const [error, setError] = useState<unknown>();
    const [activeCitation, setActiveCitation] = useState<string>();
    const [activeAnalysisPanelTab, setActiveAnalysisPanelTab] = useState<AnalysisPanelTabs | undefined>(undefined);
    const [answer, setAnswer] = useState<AskResponse>();

    const [resumeText, setResumeText] = useState<string>("");
    const [jobDescription, setJobDescription] = useState<string>("");

    const [fullScreenAnswer, setFullScreenAnswer] = useState<null | { answer: AskResponse }>(null);
    const answerRef = useRef<HTMLDivElement | null>(null);

    const makeApiRequest = async (question: string) => {
        lastQuestionRef.current = question;

        error && setError(undefined);
        setIsLoading(true);
        setActiveCitation(undefined);
        setActiveAnalysisPanelTab(undefined);

        const request: AskRequest = {
            question,
            approach: "retrieve_then_read"
        };

        let result = {} as AskResponse;
        try {
            result = await askApi(request);
        } catch (e) {
            setError(e);
        } finally {
            setIsLoading(false);
        }
        setAnswer(result);
    };

    const onAnalyzeClick = () => {
        if (!resumeText.trim() || !jobDescription.trim()) {
            setError("Please provide both resume text and job description");
            return;
        }

        const question = `Analyze this resume against the job description:
        
RESUME:
${resumeText}

JOB DESCRIPTION:
${jobDescription}

Please provide:
1. Match percentage score
2. Matching skills found
3. Missing skills/requirements
4. Experience gap analysis
5. Recommended improvements
6. Suggested interview preparation topics`;

        makeApiRequest(question);
    };

    const isLongAnswer = (content: string) => {
        if (!content) return false;
        const lineCount = content.split("\n").length;
        if (lineCount > 8) return true;
        // Fallback: check rendered height after render
        if (answerRef.current && answerRef.current.offsetHeight > 400) return true;
        return false;
    };

    useEffect(() => {
        if (answer && answer.answer) {
            // Wait for DOM update
            setTimeout(() => {
                if (isLongAnswer(answer.answer)) {
                    setFullScreenAnswer({ answer });
                }
            }, 100);
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [answer]);

    return (
        <TwoColumnLayout
            left={
                <>
                    <SettingsButton className={styles.settingsButton} onClick={() => {}} />
                    <h2>🎯 AI Career Navigator - Resume Analysis</h2>
                    <p>Upload your resume and job description to get AI-powered career guidance</p>
                    <div className={styles.resumeInputSection}>
                        <label htmlFor="resumeText">
                            <strong>Your Resume:</strong>
                        </label>
                        <textarea
                            id="resumeText"
                            className={styles.textArea}
                            placeholder="Paste your resume text here..."
                            value={resumeText}
                            onChange={e => setResumeText(e.target.value)}
                            rows={10}
                        />
                    </div>
                    <div className={styles.jobInputSection}>
                        <label htmlFor="jobDescription">
                            <strong>Target Job Description:</strong>
                        </label>
                        <textarea
                            id="jobDescription"
                            className={styles.textArea}
                            placeholder="Paste the job description you're targeting..."
                            value={jobDescription}
                            onChange={e => setJobDescription(e.target.value)}
                            rows={8}
                        />
                    </div>
                    <QuestionInput
                        placeholder="Ask follow-up questions about your analysis..."
                        disabled={isLoading}
                        onSend={question => makeApiRequest(question)}
                    />
                    <button
                        className={`${styles.analyzeButton} ${!resumeText.trim() || !jobDescription.trim() ? styles.disabled : ""}`}
                        onClick={onAnalyzeClick}
                        disabled={isLoading || !resumeText.trim() || !jobDescription.trim()}
                    >
                        {isLoading ? "Analyzing..." : "🔍 Analyze Resume Match"}
                    </button>
                </>
            }
            right={
                <div style={{ width: "100%" }}>
                    {isLoading && <Spinner />}
                    {!lastQuestionRef.current && (
                        <div className={styles.welcomeContainer}>
                            <h3>Welcome to AI Career Navigator! 🚀</h3>
                            <h4>Features:</h4>
                            <ul>
                                <li>📊 Resume-Job Match Percentage</li>
                                <li>🎯 Skill Gap Analysis</li>
                                <li>💡 Personalized Recommendations</li>
                                <li>🎭 Interview Question Generation</li>
                                <li>✨ Resume Enhancement Suggestions</li>
                            </ul>
                        </div>
                    )}
                    {!isLoading && answer && !error && !fullScreenAnswer && (
                        <div className={styles.oneshotAnswerContainer} ref={answerRef}>
                            <Answer
                                answer={{
                                    message: { content: answer?.answer || "", role: "assistant" },
                                    delta: { content: "", role: "assistant" },
                                    context: answer?.context || { data_points: [], followup_questions: null, thoughts: [] },
                                    session_state: {}
                                }}
                                index={0}
                                speechConfig={{ speechUrls: [], setSpeechUrls: () => {}, audio: new Audio(), isPlaying: false, setIsPlaying: () => {} }}
                                isStreaming={false}
                                onCitationClicked={setActiveCitation}
                                onThoughtProcessClicked={() => setActiveAnalysisPanelTab(AnalysisPanelTabs.ThoughtProcessTab)}
                                onSupportingContentClicked={() => setActiveAnalysisPanelTab(AnalysisPanelTabs.SupportingContentTab)}
                                onFollowupQuestionClicked={q => makeApiRequest(q)}
                                showFollowupQuestions={false}
                            />
                        </div>
                    )}
                    {fullScreenAnswer && <FullScreenAnswer answer={fullScreenAnswer.answer.answer} onClose={() => setFullScreenAnswer(null)} backToHome />}
                    {error ? (
                        <div className={styles.oneshotAnswerContainer}>
                            <AnswerError error={error.toString()} onRetry={() => makeApiRequest(lastQuestionRef.current)} />
                        </div>
                    ) : null}
                    {activeCitation && (
                        <AnalysisPanel
                            className={styles.oneshotAnalysisPanel}
                            activeCitation={activeCitation}
                            onActiveTabChanged={(tab: AnalysisPanelTabs) => setActiveAnalysisPanelTab(tab)}
                            citationHeight="600px"
                            answer={{
                                message: { content: answer?.answer || "", role: "assistant" },
                                delta: { content: "", role: "assistant" },
                                context: answer?.context || { data_points: [], followup_questions: null, thoughts: [] },
                                session_state: {}
                            }}
                            activeTab={activeAnalysisPanelTab || AnalysisPanelTabs.ThoughtProcessTab}
                        />
                    )}
                </div>
            }
        />
    );
}
