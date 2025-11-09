import { useRef, useState, useEffect, useContext, useLayoutEffect } from "react";
import { useTranslation } from "react-i18next";
import { Helmet } from "react-helmet-async";
import { Panel, DefaultButton, CommandBarButton, IconButton, Dialog, Stack, TextField } from "@fluentui/react";
import readNDJSONStream from "ndjson-readablestream";
import { SquareRegular, ShieldLockRegular, ErrorCircleRegular } from "@fluentui/react-icons";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import uuid4 from "uuid4";
import { isEmpty } from "lodash-es";
import DOMPurify from "dompurify";

import appLogo from "../../assets/applogo.svg";
import styles from "./Chat.module.css";

import {
    chatApi,
    configApi,
    RetrievalMode,
    ChatAppResponse,
    ChatAppResponseOrError,
    ChatAppRequest,
    ResponseMessage,
    VectorFields,
    GPT4VInput,
    SpeechConfig
} from "../../api";
import { Answer, AnswerError, AnswerLoading } from "../../components/Answer";
import { QuestionInput } from "../../components/QuestionInput";
import { ExampleList } from "../../components/Example";
import { UserChatMessage } from "../../components/UserChatMessage";
import { AnalysisPanel, AnalysisPanelTabs } from "../../components/AnalysisPanel";
import { HistoryPanel } from "../../components/HistoryPanel";
import { HistoryProviderOptions, useHistoryManager } from "../../components/HistoryProviders";
import { HistoryButton } from "../../components/HistoryButton";
import { SettingsButton } from "../../components/SettingsButton";
import { ClearChatButton } from "../../components/ClearChatButton";
import { UploadFile } from "../../components/UploadFile";
import { useLogin, getToken, requireAccessControl } from "../../authConfig";
import { useMsal } from "@azure/msal-react";
import { TokenClaimsDisplay } from "../../components/TokenClaimsDisplay";
import { LoginContext } from "../../loginContext";
import { LanguagePicker } from "../../i18n/LanguagePicker";
import { Settings } from "../../components/Settings/Settings";
import { Hero3D } from "../../components/Hero3D";
import { CareerDashboard } from "../../components/CareerDashboard";
import { AppStateContext } from "../../state/AppProvider";
import { useFeedback } from "../../components/Feedback";
import { ChatHistoryLoadingState, Conversation, Answers } from "../../types/chat";
import FullScreenAnswer from "../../components/FullScreenAnswer";

const Chat = () => {
    const [isConfigPanelOpen, setIsConfigPanelOpen] = useState(false);
    const [isHistoryPanelOpen, setIsHistoryPanelOpen] = useState(false);
    const [promptTemplate, setPromptTemplate] = useState<string>("");
    const [temperature, setTemperature] = useState<number>(0.3);
    const [seed, setSeed] = useState<number | null>(null);
    const [minimumRerankerScore, setMinimumRerankerScore] = useState<number>(0);
    const [minimumSearchScore, setMinimumSearchScore] = useState<number>(0);
    const [retrieveCount, setRetrieveCount] = useState<number>(3);
    const [maxSubqueryCount, setMaxSubqueryCount] = useState<number>(10);
    const [resultsMergeStrategy, setResultsMergeStrategy] = useState<string>("interleaved");
    const [retrievalMode, setRetrievalMode] = useState<RetrievalMode>(RetrievalMode.Hybrid);
    const [useSemanticRanker, setUseSemanticRanker] = useState<boolean>(true);
    const [useQueryRewriting, setUseQueryRewriting] = useState<boolean>(false);
    const [reasoningEffort, setReasoningEffort] = useState<string>("");
    const [streamingEnabled, setStreamingEnabled] = useState<boolean>(true);
    const [shouldStream, setShouldStream] = useState<boolean>(true);
    const [useSemanticCaptions, setUseSemanticCaptions] = useState<boolean>(false);
    const [includeCategory, setIncludeCategory] = useState<string>("");
    const [excludeCategory, setExcludeCategory] = useState<string>("");
    const [useSuggestFollowupQuestions, setUseSuggestFollowupQuestions] = useState<boolean>(false);
    const [vectorFields, setVectorFields] = useState<VectorFields>(VectorFields.TextAndImageEmbeddings);
    const [useOidSecurityFilter, setUseOidSecurityFilter] = useState<boolean>(false);
    const [useGroupsSecurityFilter, setUseGroupsSecurityFilter] = useState<boolean>(false);
    const [gpt4vInput, setGPT4VInput] = useState<GPT4VInput>(GPT4VInput.TextAndImages);
    const [useGPT4V, setUseGPT4V] = useState<boolean>(false);

    const lastQuestionRef = useRef<string>("");
    const chatContainerRef = useRef<HTMLDivElement | null>(null);
    const answerRefs = useRef<(HTMLDivElement | null)[]>([]);

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [isStreaming, setIsStreaming] = useState<boolean>(false);
    const [error, setError] = useState<unknown>();

    const [activeCitation, setActiveCitation] = useState<string>();
    const [activeAnalysisPanelTab, setActiveAnalysisPanelTab] = useState<AnalysisPanelTabs | undefined>(undefined);

    const [selectedAnswer, setSelectedAnswer] = useState<number>(0);
    const [answers, setAnswers] = useState<[user: string, response: ChatAppResponse][]>([]);
    const [streamedAnswers, setStreamedAnswers] = useState<[user: string, response: ChatAppResponse][]>([]);
    const [speechUrls, setSpeechUrls] = useState<(string | null)[]>([]);

    const [showGPT4VOptions, setShowGPT4VOptions] = useState<boolean>(false);
    const [showSemanticRankerOption, setShowSemanticRankerOption] = useState<boolean>(false);
    const [showQueryRewritingOption, setShowQueryRewritingOption] = useState<boolean>(false);
    const [showReasoningEffortOption, setShowReasoningEffortOption] = useState<boolean>(false);
    const [showVectorOption, setShowVectorOption] = useState<boolean>(false);
    const [showUserUpload, setShowUserUpload] = useState<boolean>(false);
    const [showLanguagePicker, setshowLanguagePicker] = useState<boolean>(false);
    const [showSpeechInput, setShowSpeechInput] = useState<boolean>(false);
    const [showSpeechOutputBrowser, setShowSpeechOutputBrowser] = useState<boolean>(false);
    const [showSpeechOutputAzure, setShowSpeechOutputAzure] = useState<boolean>(false);
    const [showChatHistoryBrowser, setShowChatHistoryBrowser] = useState<boolean>(false);
    const [showChatHistoryCosmos, setShowChatHistoryCosmos] = useState<boolean>(false);
    const [showAgenticRetrievalOption, setShowAgenticRetrievalOption] = useState<boolean>(false);
    const [useAgenticRetrieval, setUseAgenticRetrieval] = useState<boolean>(false);

    const audio = useRef(new Audio()).current;
    const [isPlaying, setIsPlaying] = useState(false);

    const speechConfig: SpeechConfig = {
        speechUrls,
        setSpeechUrls,
        audio,
        isPlaying,
        setIsPlaying
    };

    const [showAuthMessage, setShowAuthMessage] = useState<boolean>(false);

    const { instance } = useMsal();
    const appStateContext = useContext(AppStateContext);
    const FEEDBACK_ENABLED = appStateContext?.state.feedbackEnabled && appStateContext.state.isCosmosDBAvailable?.cosmosDB;
    const CHAT_HISTORY_ENABLED = appStateContext?.state.isCosmosDBAvailable?.cosmosDB && appStateContext?.state.chatHistoryEnabled;
    const UI_FEEDBACK = appStateContext?.state.frontendSettings?.feedback_enabled || false;
    const { updateFeedback } = useFeedback();

    // For showing chat history
    const [chatHistoryLoadingState, setChatHistoryLoadingState] = useState<ChatHistoryLoadingState>(ChatHistoryLoadingState.Loading);
    const [historyList, setHistoryList] = useState<Conversation[] | null>(null);
    const [conversationExists, setConversationExists] = useState<boolean>(false);

    // Chat view state management
    const [showCareerDashboard, setShowCareerDashboard] = useState<boolean>(true);
    const [activeFeature, setActiveFeature] = useState<string>("resume");

    const [fullScreenAnswer, setFullScreenAnswer] = useState<null | { answer: [string, ChatAppResponse]; index: number }>(null);
    const [pendingCheckIndex, setPendingCheckIndex] = useState<number | null>(null);

    const getConfig = async () => {
        configApi().then(config => {
            setShowGPT4VOptions(config.showGPT4VOptions);
            if (config.showGPT4VOptions) {
                setUseGPT4V(true);
            }
            setUseSemanticRanker(config.showSemanticRankerOption);
            setShowSemanticRankerOption(config.showSemanticRankerOption);
            setUseQueryRewriting(config.showQueryRewritingOption);
            setShowQueryRewritingOption(config.showQueryRewritingOption);
            setShowReasoningEffortOption(config.showReasoningEffortOption);
            setStreamingEnabled(config.streamingEnabled);
            if (!config.streamingEnabled) {
                setShouldStream(false);
            }
            if (config.showReasoningEffortOption) {
                setReasoningEffort(config.defaultReasoningEffort);
            }
            setShowVectorOption(config.showVectorOption);
            if (!config.showVectorOption) {
                setRetrievalMode(RetrievalMode.Text);
            }
            setShowUserUpload(config.showUserUpload);
            setshowLanguagePicker(config.showLanguagePicker);
            setShowSpeechInput(config.showSpeechInput);
            setShowSpeechOutputBrowser(config.showSpeechOutputBrowser);
            setShowSpeechOutputAzure(config.showSpeechOutputAzure);
            setShowChatHistoryBrowser(config.showChatHistoryBrowser);
            setShowChatHistoryCosmos(config.showChatHistoryCosmos);
            setShowAgenticRetrievalOption(config.showAgenticRetrievalOption);
            setUseAgenticRetrieval(config.showAgenticRetrievalOption);
            if (config.showAgenticRetrievalOption) {
                setRetrieveCount(10);
            }
        });
    };

    const handleAsyncRequest = async (question: string, answers: [string, ChatAppResponse][], responseBody: ReadableStream<any>) => {
        let answer: string = "";
        let askResponse: ChatAppResponse = {} as ChatAppResponse;

        const updateState = (newContent: string) => {
            return new Promise(resolve => {
                setTimeout(() => {
                    answer += newContent;
                    const latestResponse: ChatAppResponse = {
                        ...askResponse,
                        message: { content: answer, role: askResponse.message.role }
                    };
                    setStreamedAnswers([...answers, [question, latestResponse]]);
                    resolve(null);
                }, 33);
            });
        };
        try {
            setIsStreaming(true);
            for await (const event of readNDJSONStream(responseBody)) {
                if (event["context"] && event["context"]["data_points"]) {
                    event["message"] = event["delta"];
                    askResponse = event as ChatAppResponse;
                } else if (event["delta"] && event["delta"]["content"]) {
                    setIsLoading(false);
                    await updateState(event["delta"]["content"]);
                } else if (event["context"]) {
                    // Update context with new keys from latest event
                    askResponse.context = { ...askResponse.context, ...event["context"] };
                } else if (event["error"]) {
                    throw Error(event["error"]);
                }
            }
        } finally {
            setIsStreaming(false);
        }
        const fullResponse: ChatAppResponse = {
            ...askResponse,
            message: { content: answer, role: askResponse.message.role }
        };
        return fullResponse;
    };

    const client = useLogin ? instance : undefined;
    const { loggedIn } = useContext(LoginContext);

    const historyProvider: HistoryProviderOptions = (() => {
        if (useLogin && showChatHistoryCosmos) return HistoryProviderOptions.CosmosDB;
        if (showChatHistoryBrowser) return HistoryProviderOptions.IndexedDB;
        return HistoryProviderOptions.None;
    })();
    const historyManager = useHistoryManager(historyProvider);

    const makeApiRequest = async (question: string) => {
        lastQuestionRef.current = question;

        error && setError(undefined);
        setIsLoading(true);
        setActiveCitation(undefined);
        setActiveAnalysisPanelTab(undefined);
        setShowCareerDashboard(false);

        const token = client ? await getToken(client) : undefined;

        try {
            const messages: ResponseMessage[] = answers.flatMap(a => [
                { content: a[0], role: "user" },
                { content: a[1].message.content, role: "assistant" }
            ]);

            const request: ChatAppRequest = {
                messages: [...messages, { content: question, role: "user" }],
                context: {
                    overrides: {
                        prompt_template: promptTemplate.length === 0 ? undefined : promptTemplate,
                        include_category: includeCategory.length === 0 ? undefined : includeCategory,
                        exclude_category: excludeCategory.length === 0 ? undefined : excludeCategory,
                        top: retrieveCount,
                        max_subqueries: maxSubqueryCount,
                        results_merge_strategy: resultsMergeStrategy,
                        temperature: temperature,
                        minimum_reranker_score: minimumRerankerScore,
                        minimum_search_score: minimumSearchScore,
                        retrieval_mode: retrievalMode,
                        semantic_ranker: useSemanticRanker,
                        semantic_captions: useSemanticCaptions,
                        query_rewriting: useQueryRewriting,
                        reasoning_effort: reasoningEffort,
                        suggest_followup_questions: useSuggestFollowupQuestions,
                        use_oid_security_filter: useOidSecurityFilter,
                        use_groups_security_filter: useGroupsSecurityFilter,
                        vector_fields: vectorFields,
                        use_gpt4v: useGPT4V,
                        gpt4v_input: gpt4vInput,
                        language: i18n.language,
                        use_agentic_retrieval: useAgenticRetrieval,
                        ...(seed !== null ? { seed: seed } : {})
                    }
                },
                // AI Chat Protocol: Client must pass on any session state received from the server
                session_state: answers.length ? answers[answers.length - 1][1].session_state : null
            };

            const response = await chatApi(request, shouldStream, token);
            if (!response.body) {
                throw Error("No response body");
            }
            if (response.status > 299 || !response.ok) {
                throw Error(`Request failed with status ${response.status}`);
            }
            if (shouldStream) {
                const parsedResponse: ChatAppResponse = await handleAsyncRequest(question, answers, response.body);
                setAnswers(prev => {
                    const newAnswers: [string, ChatAppResponse][] = [...prev, [question, parsedResponse]];
                    setPendingCheckIndex(newAnswers.length - 1);
                    return newAnswers;
                });
                if (typeof parsedResponse.session_state === "string" && parsedResponse.session_state !== "") {
                    const token = client ? await getToken(client) : undefined;
                    historyManager.addItem(parsedResponse.session_state, [...answers, [question, parsedResponse]], token);
                }
            } else {
                const parsedResponse: ChatAppResponseOrError = await response.json();
                if (parsedResponse.error) {
                    throw Error(parsedResponse.error);
                }
                setAnswers(prev => {
                    const newAnswers: [string, ChatAppResponse][] = [...prev, [question, parsedResponse as ChatAppResponse]];
                    setPendingCheckIndex(newAnswers.length - 1);
                    return newAnswers;
                });
                if (typeof parsedResponse.session_state === "string" && parsedResponse.session_state !== "") {
                    const token = client ? await getToken(client) : undefined;
                    historyManager.addItem(parsedResponse.session_state, [...answers, [question, parsedResponse as ChatAppResponse]], token);
                }
            }
            setSpeechUrls([...speechUrls, null]);
        } catch (e) {
            setError(e);
        } finally {
            setIsLoading(false);
        }
    };

    const clearChat = () => {
        lastQuestionRef.current = "";
        error && setError(undefined);
        setActiveCitation(undefined);
        setActiveAnalysisPanelTab(undefined);
        setAnswers([]);
        setSpeechUrls([]);
        setStreamedAnswers([]);
        setIsLoading(false);
        setIsStreaming(false);
        setShowCareerDashboard(true);
    };

    const handleSettingsChange = (field: string, value: any) => {
        switch (field) {
            case "promptTemplate":
                setPromptTemplate(value);
                break;
            case "temperature":
                setTemperature(value);
                break;
            case "seed":
                setSeed(value);
                break;
            case "minimumRerankerScore":
                setMinimumRerankerScore(value);
                break;
            case "minimumSearchScore":
                setMinimumSearchScore(value);
                break;
            case "retrieveCount":
                setRetrieveCount(value);
                break;
            case "maxSubqueryCount":
                setMaxSubqueryCount(value);
                break;
            case "resultsMergeStrategy":
                setResultsMergeStrategy(value);
                break;
            case "useSemanticRanker":
                setUseSemanticRanker(value);
                break;
            case "useQueryRewriting":
                setUseQueryRewriting(value);
                break;
            case "reasoningEffort":
                setReasoningEffort(value);
                break;
            case "useSemanticCaptions":
                setUseSemanticCaptions(value);
                break;
            case "excludeCategory":
                setExcludeCategory(value);
                break;
            case "includeCategory":
                setIncludeCategory(value);
                break;
            case "useOidSecurityFilter":
                setUseOidSecurityFilter(value);
                break;
            case "useGroupsSecurityFilter":
                setUseGroupsSecurityFilter(value);
                break;
            case "shouldStream":
                setShouldStream(value);
                break;
            case "useSuggestFollowupQuestions":
                setUseSuggestFollowupQuestions(value);
                break;
            case "useGPT4V":
                setUseGPT4V(value);
                break;
            case "gpt4vInput":
                setGPT4VInput(value);
                break;
            case "vectorFields":
                setVectorFields(value);
                break;
            case "retrievalMode":
                setRetrievalMode(value);
                break;
            case "useAgenticRetrieval":
                setUseAgenticRetrieval(value);
        }
    };

    const onExampleClicked = (example: string) => {
        makeApiRequest(example);
    };

    const onShowCitation = (citation: string, index: number) => {
        setActiveCitation(citation);
        setActiveAnalysisPanelTab(AnalysisPanelTabs.SupportingContentTab);
        setSelectedAnswer(index);
    };

    const onToggleTab = (tab: AnalysisPanelTabs, index: number) => {
        if (activeAnalysisPanelTab === tab && selectedAnswer === index) {
            setActiveAnalysisPanelTab(undefined);
        } else {
            setActiveAnalysisPanelTab(tab);
        }

        setSelectedAnswer(index);
    };

    const { t, i18n } = useTranslation();

    useEffect(() => {
        if (pendingCheckIndex !== null && answerRefs.current[pendingCheckIndex]) {
            const el = answerRefs.current[pendingCheckIndex];
            if (el) {
                const lineCount = el.innerText.split("\n").length;
                if (el.scrollHeight > 400 || lineCount > 8) {
                    setFullScreenAnswer({ answer: answers[pendingCheckIndex], index: pendingCheckIndex });
                }
            }
            setPendingCheckIndex(null);
        }
    }, [pendingCheckIndex, answers]);

    // Handle completion of each feature
    const handleFeatureComplete = (feature: string) => {
        switch (feature) {
            case "resume":
                setActiveFeature("skillgap");
                break;
            case "skillgap":
                setActiveFeature("interview");
                break;
            case "interview":
                setActiveFeature("chat");
                setShowCareerDashboard(false);
                break;
            default:
                break;
        }
    };

    return (
        <div className={styles.chatContainer}>
            {/* Header with controls */}
            <div className={styles.chatHeader}>
                <div className={styles.headerControls}>
                    <SettingsButton onClick={() => setIsConfigPanelOpen(true)} />
                    <HistoryButton onClick={() => setIsHistoryPanelOpen(true)} />
                    <ClearChatButton onClick={clearChat} disabled={!lastQuestionRef.current || isLoading} />
                </div>
            </div>

            {/* Main container with career dashboard and chat */}
            <div className={styles.mainContent}>
                {/* Career Dashboard - shown initially */}
                {showCareerDashboard && (
                    <div className={styles.careerDashboardContainer}>
                        <CareerDashboard activeFeature={activeFeature} onFeatureComplete={handleFeatureComplete} />
                    </div>
                )}

                {/* Chat interface - always present but initially hidden */}
                <div className={`${styles.chatMainContainer} ${!showCareerDashboard ? styles.chatMainContainerActive : ""}`}>
                    {/* Examples section - only show when no conversation started */}
                    {answers.length === 0 && !showCareerDashboard && (
                        <div className={styles.examplesSection}>
                            <ExampleList onExampleClicked={onExampleClicked} useGPT4V={useGPT4V} />
                        </div>
                    )}

                    {/* Chat messages - adaptive height container */}
                    <div className={styles.chatMessagesContainer} ref={chatContainerRef}>
                        {isStreaming &&
                            streamedAnswers.map((streamedAnswer, index) => (
                                <div key={index} className={styles.messageGroup}>
                                    <UserChatMessage message={streamedAnswer[0]} />
                                    <div className={styles.chatMessageGpt}>
                                        <Answer
                                            isStreaming={true}
                                            key={index}
                                            answer={streamedAnswer[1]}
                                            index={index}
                                            speechConfig={speechConfig}
                                            isSelected={false}
                                            onCitationClicked={c => onShowCitation(c, index)}
                                            onThoughtProcessClicked={() => onToggleTab(AnalysisPanelTabs.ThoughtProcessTab, index)}
                                            onSupportingContentClicked={() => onToggleTab(AnalysisPanelTabs.SupportingContentTab, index)}
                                            onFollowupQuestionClicked={q => makeApiRequest(q)}
                                            showFollowupQuestions={useSuggestFollowupQuestions && answers.length - 1 === index}
                                            showSpeechOutputAzure={showSpeechOutputAzure}
                                            showSpeechOutputBrowser={showSpeechOutputBrowser}
                                        />
                                    </div>
                                </div>
                            ))}
                        {!isStreaming &&
                            answers.map((answer, index) => (
                                <div key={index} className={styles.messageGroup}>
                                    <UserChatMessage message={answer[0]} />
                                    <div className={styles.chatMessageGpt}>
                                        <div ref={el => (answerRefs.current[index] = el)}>
                                            <Answer
                                                isStreaming={false}
                                                key={index}
                                                answer={answer[1]}
                                                index={index}
                                                speechConfig={speechConfig}
                                                isSelected={selectedAnswer === index && activeAnalysisPanelTab !== undefined}
                                                onCitationClicked={c => onShowCitation(c, index)}
                                                onThoughtProcessClicked={() => onToggleTab(AnalysisPanelTabs.ThoughtProcessTab, index)}
                                                onSupportingContentClicked={() => onToggleTab(AnalysisPanelTabs.SupportingContentTab, index)}
                                                onFollowupQuestionClicked={q => makeApiRequest(q)}
                                                showFollowupQuestions={useSuggestFollowupQuestions && answers.length - 1 === index}
                                                showSpeechOutputAzure={showSpeechOutputAzure}
                                                showSpeechOutputBrowser={showSpeechOutputBrowser}
                                            />
                                        </div>
                                    </div>
                                </div>
                            ))}
                        {isLoading && (
                            <div className={styles.messageGroup}>
                                <UserChatMessage message={lastQuestionRef.current} />
                                <div className={styles.chatMessageGptMinWidth}>
                                    <AnswerLoading />
                                </div>
                            </div>
                        )}
                        {error ? (
                            <div className={styles.messageGroup}>
                                <UserChatMessage message={lastQuestionRef.current} />
                                <div className={styles.chatMessageGptMinWidth}>
                                    <AnswerError error={error.toString()} onRetry={() => makeApiRequest(lastQuestionRef.current)} />
                                </div>
                            </div>
                        ) : null}
                    </div>

                    {/* Input section - fixed at bottom */}
                    <div className={styles.inputSection}>
                        <QuestionInput
                            clearOnSend
                            placeholder="Ask me about your career, resume, or interview preparation..."
                            disabled={isLoading}
                            onSend={question => makeApiRequest(question)}
                            showSpeechInput={false}
                        />
                    </div>
                </div>
            </div>

            {/* Panels remain unchanged */}
            <Panel
                headerText="Configure answer generation"
                isOpen={isConfigPanelOpen}
                isBlocking={false}
                onDismiss={() => setIsConfigPanelOpen(false)}
                closeButtonAriaLabel="Close"
                onRenderFooterContent={() => <DefaultButton onClick={() => setIsConfigPanelOpen(false)}>Close</DefaultButton>}
                isFooterAtBottom={true}
            >
                <div style={{ padding: "20px" }}>
                    <p>Settings panel - configuration options will be available here.</p>
                    <Stack tokens={{ childrenGap: 10 }}>
                        <TextField
                            label="Temperature"
                            value={temperature.toString()}
                            onChange={(_, newValue) => setTemperature(parseFloat(newValue || "0.3"))}
                        />
                        <TextField
                            label="Retrieve Count"
                            value={retrieveCount.toString()}
                            onChange={(_, newValue) => setRetrieveCount(parseInt(newValue || "3"))}
                        />
                    </Stack>
                </div>
            </Panel>

            {CHAT_HISTORY_ENABLED && (
                <HistoryPanel
                    provider={HistoryProviderOptions.CosmosDB}
                    isOpen={isHistoryPanelOpen}
                    notify={false}
                    onClose={() => setIsHistoryPanelOpen(false)}
                    onChatSelected={answers => {
                        setAnswers(answers);
                        setIsHistoryPanelOpen(false);
                    }}
                />
            )}

            {/* Panel for citations and analysis */}
            {answers.length > 0 && activeAnalysisPanelTab && (
                <Panel
                    headerText="Analysis"
                    isOpen={activeAnalysisPanelTab !== undefined}
                    isBlocking={false}
                    onDismiss={() => setActiveAnalysisPanelTab(undefined)}
                    closeButtonAriaLabel="Close"
                    onRenderFooterContent={() => <DefaultButton onClick={() => setActiveAnalysisPanelTab(undefined)}>Close</DefaultButton>}
                    isFooterAtBottom={true}
                >
                    <AnalysisPanel
                        className={styles.analysisPanel}
                        activeCitation={activeCitation}
                        onActiveTabChanged={x => onToggleTab(x, selectedAnswer)}
                        citationHeight="600px"
                        answer={answers[selectedAnswer][1]}
                        activeTab={activeAnalysisPanelTab}
                    />
                </Panel>
            )}

            {fullScreenAnswer && (
                <FullScreenAnswer
                    answer={
                        <>
                            <UserChatMessage message={fullScreenAnswer.answer[0]} />
                            <div className={styles.chatMessageGpt}>
                                <Answer
                                    isStreaming={false}
                                    key={fullScreenAnswer.index}
                                    answer={fullScreenAnswer.answer[1]}
                                    index={fullScreenAnswer.index}
                                    speechConfig={speechConfig}
                                    isSelected={selectedAnswer === fullScreenAnswer.index && activeAnalysisPanelTab !== undefined}
                                    onCitationClicked={c => onShowCitation(c, fullScreenAnswer.index)}
                                    onThoughtProcessClicked={() => onToggleTab(AnalysisPanelTabs.ThoughtProcessTab, fullScreenAnswer.index)}
                                    onSupportingContentClicked={() => onToggleTab(AnalysisPanelTabs.SupportingContentTab, fullScreenAnswer.index)}
                                    onFollowupQuestionClicked={q => makeApiRequest(q)}
                                    showFollowupQuestions={useSuggestFollowupQuestions && answers.length - 1 === fullScreenAnswer.index}
                                    showSpeechOutputAzure={showSpeechOutputAzure}
                                    showSpeechOutputBrowser={showSpeechOutputBrowser}
                                />
                            </div>
                        </>
                    }
                    onClose={() => setFullScreenAnswer(null)}
                />
            )}
        </div>
    );
};

export default Chat;
