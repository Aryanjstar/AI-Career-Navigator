import React, { useState, useCallback, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useDropzone } from "react-dropzone";
import {
    DocumentArrowUpIcon,
    ChartBarIcon,
    QuestionMarkCircleIcon,
    SparklesIcon,
    CheckCircleIcon,
    ExclamationTriangleIcon,
    LightBulbIcon,
    ArrowTrendingUpIcon
} from "@heroicons/react/24/outline";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from "recharts";
import toast from "react-hot-toast";
import { ShimmerEffect, ShimmerCard } from "./ui/ShimmerEffect";
import { SplitText, TypingText } from "./ui/SplitText";
import { SocialShare } from "./SocialShare";
import { useAnalytics, trackResumeUpload, trackAnalysisStart, trackAnalysisComplete } from "./AnalyticsTracker";

interface AnalysisResult {
    matchScore: number;
    skillsPresent: string[];
    skillsMissing: string[];
    interviewQuestions: {
        technical: string[];
        behavioral: string[];
    };
    suggestions: string[];
    salaryEstimate: {
        min: number;
        max: number;
        currency: string;
    };
}

interface CareerDashboardProps {
    className?: string;
    activeFeature: string;
    onFeatureComplete: (feature: string) => void;
}

const COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"];

export const CareerDashboard: React.FC<CareerDashboardProps> = ({ className, activeFeature, onFeatureComplete }) => {
    const [activeTab, setActiveTab] = useState("upload");
    const [resumeFile, setResumeFile] = useState<File | null>(null);
    const [jobDescription, setJobDescription] = useState("");
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
    const analytics = useAnalytics();

    // Update active tab when activeFeature changes
    useEffect(() => {
        setActiveTab(activeFeature);
    }, [activeFeature]);

    // File upload handler
    const onDrop = useCallback(
        (acceptedFiles: File[]) => {
            const file = acceptedFiles[0];
            if (file) {
                setResumeFile(file);
                trackResumeUpload(file.type, file.size);
                analytics.trackUserAction("resume_uploaded", {
                    fileType: file.type,
                    fileSize: file.size,
                    fileName: file.name
                });
                toast.success(`Resume uploaded: ${file.name}`);
            }
        },
        [analytics]
    );

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            "application/pdf": [".pdf"],
            "application/msword": [".doc"],
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
            "text/plain": [".txt"]
        },
        maxFiles: 1
    });

    // Handle analysis completion
    const handleAnalysis = async () => {
        if (!resumeFile || !jobDescription.trim()) {
            toast.error("Please upload a resume and add job description");
            return;
        }

        setIsAnalyzing(true);
        const startTime = Date.now();
        trackAnalysisStart("resume_job_match");
        analytics.trackUserAction("analysis_started", {
            hasResume: !!resumeFile,
            jobDescriptionLength: jobDescription.length
        });

        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 3000));

        // Mock analysis result
        const mockResult: AnalysisResult = {
            matchScore: 78,
            skillsPresent: ["React.js", "TypeScript", "Node.js", "Python", "Git", "Azure"],
            skillsMissing: ["Kubernetes", "Docker", "GraphQL", "MongoDB"],
            interviewQuestions: {
                technical: [
                    "Explain the difference between useState and useEffect in React",
                    "How would you optimize a slow React application?",
                    "Describe your experience with TypeScript and its benefits",
                    "How do you handle state management in large applications?",
                    "Explain the concept of microservices architecture"
                ],
                behavioral: [
                    "Tell me about a challenging project you worked on",
                    "How do you handle tight deadlines and pressure?",
                    "Describe a time when you had to learn a new technology quickly",
                    "How do you approach problem-solving in development?",
                    "What motivates you in your career?"
                ]
            },
            suggestions: [
                "Add more details about your Azure cloud projects",
                "Highlight your TypeScript experience with specific examples",
                "Include metrics and impact of your projects",
                "Add certifications or relevant coursework",
                "Emphasize leadership and collaboration skills"
            ],
            salaryEstimate: {
                min: 80000,
                max: 120000,
                currency: "USD"
            }
        };

        const duration = Date.now() - startTime;
        trackAnalysisComplete("resume_job_match", mockResult.matchScore, duration);
        analytics.trackResumeAnalysis({
            matchScore: mockResult.matchScore,
            skillsFound: mockResult.skillsPresent.length,
            skillsMissing: mockResult.skillsMissing.length,
            analysisTime: duration
        });

        setAnalysisResult(mockResult);
        setIsAnalyzing(false);
        setActiveTab("results");
        toast.success("Analysis completed!");

        // Call the onFeatureComplete callback with current feature
        onFeatureComplete(activeFeature);
    };

    const tabs = [
        { id: "upload", label: "Resume Analysis", icon: DocumentArrowUpIcon },
        { id: "skillgap", label: "Skill Gap", icon: ChartBarIcon },
        { id: "interview", label: "Interview Prep", icon: QuestionMarkCircleIcon },
        { id: "chat", label: "Career Chat", icon: SparklesIcon }
    ];

    return (
        <div className={`flex-1 bg-gradient-to-br from-secondary-50 to-primary-50 ${className}`}>
            <div className="container mx-auto px-6 py-8">
                {/* Header */}
                <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-12">
                    <h1 className="text-4xl font-bold text-secondary-900 mb-4">🎯 AI Career Navigator Dashboard</h1>
                    <p className="text-lg text-secondary-600">Analyze your resume, identify skill gaps, and prepare for interviews with AI</p>
                </motion.div>

                {/* Tab Navigation */}
                <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="flex flex-wrap justify-center mb-8">
                    {tabs.map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center space-x-2 px-6 py-3 m-2 rounded-xl font-medium transition-all duration-300 ${
                                activeTab === tab.id ? "bg-primary-600 text-white shadow-lg" : "bg-white text-secondary-600 hover:bg-primary-50"
                            }`}
                        >
                            <tab.icon className="h-5 w-5" />
                            <span>{tab.label}</span>
                        </button>
                    ))}
                </motion.div>

                {/* Tab Content */}
                <AnimatePresence mode="wait">
                    {activeTab === "upload" && (
                        <motion.div
                            key="upload"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 20 }}
                            className="max-w-4xl mx-auto"
                        >
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                {/* Resume Upload */}
                                <div className="bg-white rounded-2xl p-8 shadow-xl">
                                    <h3 className="text-2xl font-bold text-secondary-800 mb-6 flex items-center">
                                        <DocumentArrowUpIcon className="h-6 w-6 mr-2 text-primary-600" />
                                        Upload Resume
                                    </h3>

                                    <div
                                        {...getRootProps()}
                                        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 cursor-pointer ${
                                            isDragActive ? "border-primary-500 bg-primary-50" : "border-secondary-300 hover:border-primary-400"
                                        }`}
                                    >
                                        <input {...getInputProps()} />
                                        <DocumentArrowUpIcon className="h-12 w-12 mx-auto mb-4 text-secondary-400" />
                                        {resumeFile ? (
                                            <div>
                                                <p className="text-lg font-medium text-secondary-700">✅ {resumeFile.name}</p>
                                                <p className="text-sm text-secondary-500">Click to change file</p>
                                            </div>
                                        ) : (
                                            <div>
                                                <p className="text-lg font-medium text-secondary-700">Drag & drop your resume here</p>
                                                <p className="text-sm text-secondary-500">Supports PDF, DOC, DOCX, TXT</p>
                                            </div>
                                        )}
                                    </div>
                                </div>

                                {/* Job Description */}
                                <div className="bg-white rounded-2xl p-8 shadow-xl">
                                    <h3 className="text-2xl font-bold text-secondary-800 mb-6">📝 Job Description</h3>

                                    <textarea
                                        value={jobDescription}
                                        onChange={e => setJobDescription(e.target.value)}
                                        placeholder="Paste the job description here..."
                                        className="w-full h-64 p-4 border border-secondary-300 rounded-xl resize-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                                    />

                                    <div className="mt-4 text-sm text-secondary-500">
                                        💡 Include job requirements, skills, and responsibilities for better analysis
                                    </div>
                                </div>
                            </div>

                            {/* Analyze Button */}
                            <motion.div className="text-center mt-8" whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                                <button
                                    onClick={handleAnalysis}
                                    disabled={isAnalyzing || !resumeFile || !jobDescription.trim()}
                                    className="px-12 py-4 bg-gradient-to-r from-primary-600 to-accent-500 text-white font-bold text-lg rounded-2xl shadow-xl hover:shadow-2xl disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
                                >
                                    {isAnalyzing ? (
                                        <div className="flex items-center space-x-2">
                                            <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
                                            <span>Analyzing...</span>
                                        </div>
                                    ) : (
                                        <div className="flex items-center space-x-2">
                                            <SparklesIcon className="h-6 w-6" />
                                            <span>Analyze with AI</span>
                                        </div>
                                    )}
                                </button>
                            </motion.div>
                        </motion.div>
                    )}

                    {activeTab === "results" && analysisResult && (
                        <motion.div
                            key="results"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 20 }}
                            className="max-w-6xl mx-auto"
                        >
                            {/* Match Score */}
                            <div className="bg-white rounded-2xl p-8 shadow-xl mb-8">
                                <div className="text-center">
                                    <h3 className="text-3xl font-bold text-secondary-800 mb-4">Match Score</h3>
                                    <div className="relative inline-block">
                                        <div className="w-32 h-32 rounded-full border-8 border-secondary-200 relative">
                                            <div
                                                className="absolute inset-0 rounded-full border-8 border-transparent"
                                                style={{
                                                    borderTopColor:
                                                        analysisResult.matchScore >= 80 ? "#10b981" : analysisResult.matchScore >= 60 ? "#f59e0b" : "#ef4444",
                                                    transform: `rotate(${(analysisResult.matchScore / 100) * 360}deg)`
                                                }}
                                            ></div>
                                            <div className="absolute inset-0 flex items-center justify-center">
                                                <span className="text-3xl font-bold text-secondary-800">{analysisResult.matchScore}%</span>
                                            </div>
                                        </div>
                                    </div>
                                    <p className="text-lg text-secondary-600 mt-4">
                                        {analysisResult.matchScore >= 80
                                            ? "🎉 Excellent match!"
                                            : analysisResult.matchScore >= 60
                                              ? "👍 Good match with room for improvement"
                                              : "⚠️ Needs significant improvement"}
                                    </p>
                                </div>
                            </div>

                            {/* Skills Analysis */}
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                                {/* Skills Present */}
                                <div className="bg-white rounded-2xl p-8 shadow-xl">
                                    <h3 className="text-2xl font-bold text-success-700 mb-6 flex items-center">
                                        <CheckCircleIcon className="h-6 w-6 mr-2" />
                                        Matching Skills ({analysisResult.skillsPresent.length})
                                    </h3>
                                    <div className="space-y-3">
                                        {analysisResult.skillsPresent.map((skill, index) => (
                                            <motion.div
                                                key={index}
                                                initial={{ opacity: 0, x: -20 }}
                                                animate={{ opacity: 1, x: 0 }}
                                                transition={{ delay: index * 0.1 }}
                                                className="flex items-center space-x-3 p-3 bg-success-50 rounded-lg"
                                            >
                                                <CheckCircleIcon className="h-5 w-5 text-success-600" />
                                                <span className="font-medium text-success-800">{skill}</span>
                                            </motion.div>
                                        ))}
                                    </div>
                                </div>

                                {/* Skills Missing */}
                                <div className="bg-white rounded-2xl p-8 shadow-xl">
                                    <h3 className="text-2xl font-bold text-warning-700 mb-6 flex items-center">
                                        <ExclamationTriangleIcon className="h-6 w-6 mr-2" />
                                        Missing Skills ({analysisResult.skillsMissing.length})
                                    </h3>
                                    <div className="space-y-3">
                                        {analysisResult.skillsMissing.map((skill, index) => (
                                            <motion.div
                                                key={index}
                                                initial={{ opacity: 0, x: -20 }}
                                                animate={{ opacity: 1, x: 0 }}
                                                transition={{ delay: index * 0.1 }}
                                                className="flex items-center space-x-3 p-3 bg-warning-50 rounded-lg"
                                            >
                                                <ExclamationTriangleIcon className="h-5 w-5 text-warning-600" />
                                                <span className="font-medium text-warning-800">{skill}</span>
                                            </motion.div>
                                        ))}
                                    </div>
                                </div>
                            </div>

                            {/* Salary Estimate */}
                            <div className="bg-white rounded-2xl p-8 shadow-xl mb-8">
                                <h3 className="text-2xl font-bold text-secondary-800 mb-6">💰 Salary Estimate</h3>
                                <div className="text-center">
                                    <div className="text-4xl font-bold text-primary-600 mb-2">
                                        ${analysisResult.salaryEstimate.min.toLocaleString()} - ${analysisResult.salaryEstimate.max.toLocaleString()}
                                    </div>
                                    <p className="text-secondary-600">Based on your skills and the job requirements</p>
                                </div>
                            </div>

                            {/* Suggestions */}
                            <div className="bg-white rounded-2xl p-8 shadow-xl">
                                <h3 className="text-2xl font-bold text-secondary-800 mb-6 flex items-center">
                                    <LightBulbIcon className="h-6 w-6 mr-2 text-warning-500" />
                                    AI Recommendations
                                </h3>
                                <div className="space-y-4">
                                    {analysisResult.suggestions.map((suggestion, index) => (
                                        <motion.div
                                            key={index}
                                            initial={{ opacity: 0, y: 20 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ delay: index * 0.1 }}
                                            className="flex items-start space-x-3 p-4 bg-accent-50 rounded-lg"
                                        >
                                            <LightBulbIcon className="h-5 w-5 text-accent-600 mt-1" />
                                            <span className="text-secondary-700">{suggestion}</span>
                                        </motion.div>
                                    ))}
                                </div>
                            </div>

                            {/* Level 4: Social Sharing for Results */}
                            <motion.div className="mt-8" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.8 }}>
                                <SocialShare
                                    title={`I just got a ${analysisResult.matchScore}% match score on AI Career Navigator! 🎯`}
                                    description={`My resume analysis revealed ${analysisResult.skillsPresent.length} matching skills and identified ${analysisResult.skillsMissing.length} areas for improvement. This AI tool is amazing!`}
                                    hashtags={["AICareer", "ResumeAnalysis", "CareerGrowth", "TechJobs"]}
                                />
                            </motion.div>
                        </motion.div>
                    )}

                    {activeTab === "interview" && analysisResult && (
                        <motion.div
                            key="interview"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 20 }}
                            className="max-w-6xl mx-auto"
                        >
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                {/* Technical Questions */}
                                <div className="bg-white rounded-2xl p-8 shadow-xl">
                                    <h3 className="text-2xl font-bold text-primary-700 mb-6">🔧 Technical Questions</h3>
                                    <div className="space-y-4">
                                        {analysisResult.interviewQuestions.technical.map((question, index) => (
                                            <motion.div
                                                key={index}
                                                initial={{ opacity: 0, y: 20 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                transition={{ delay: index * 0.1 }}
                                                className="p-4 bg-primary-50 rounded-lg border-l-4 border-primary-500"
                                            >
                                                <p className="text-secondary-700 font-medium">{question}</p>
                                            </motion.div>
                                        ))}
                                    </div>
                                </div>

                                {/* Behavioral Questions */}
                                <div className="bg-white rounded-2xl p-8 shadow-xl">
                                    <h3 className="text-2xl font-bold text-accent-700 mb-6">🎭 Behavioral Questions</h3>
                                    <div className="space-y-4">
                                        {analysisResult.interviewQuestions.behavioral.map((question, index) => (
                                            <motion.div
                                                key={index}
                                                initial={{ opacity: 0, y: 20 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                transition={{ delay: index * 0.1 }}
                                                className="p-4 bg-accent-50 rounded-lg border-l-4 border-accent-500"
                                            >
                                                <p className="text-secondary-700 font-medium">{question}</p>
                                            </motion.div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {activeTab === "chat" && (
                        <motion.div
                            key="chat"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: 20 }}
                            className="max-w-6xl mx-auto"
                        >
                            {/* Career Analytics Dashboard */}
                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                                {/* Skill Trends */}
                                <div className="bg-white rounded-2xl p-8 shadow-xl">
                                    <h3 className="text-2xl font-bold text-secondary-800 mb-6">📈 Skill Trends</h3>
                                    <ResponsiveContainer width="100%" height={300}>
                                        <LineChart
                                            data={[
                                                { month: "Jan", react: 85, nodejs: 70, python: 90 },
                                                { month: "Feb", react: 88, nodejs: 75, python: 92 },
                                                { month: "Mar", react: 92, nodejs: 80, python: 95 },
                                                { month: "Apr", react: 90, nodejs: 85, python: 93 },
                                                { month: "May", react: 95, nodejs: 88, python: 97 }
                                            ]}
                                        >
                                            <CartesianGrid strokeDasharray="3 3" />
                                            <XAxis dataKey="month" />
                                            <YAxis />
                                            <Tooltip />
                                            <Line type="monotone" dataKey="react" stroke="#3b82f6" strokeWidth={3} />
                                            <Line type="monotone" dataKey="nodejs" stroke="#10b981" strokeWidth={3} />
                                            <Line type="monotone" dataKey="python" stroke="#f59e0b" strokeWidth={3} />
                                        </LineChart>
                                    </ResponsiveContainer>
                                </div>

                                {/* Job Market Insights */}
                                <div className="bg-white rounded-2xl p-8 shadow-xl">
                                    <h3 className="text-2xl font-bold text-secondary-800 mb-6">💼 Job Market Insights</h3>
                                    <ResponsiveContainer width="100%" height={300}>
                                        <BarChart
                                            data={[
                                                { role: "Frontend", demand: 85 },
                                                { role: "Backend", demand: 78 },
                                                { role: "Full Stack", demand: 92 },
                                                { role: "DevOps", demand: 70 },
                                                { role: "ML Engineer", demand: 88 }
                                            ]}
                                        >
                                            <CartesianGrid strokeDasharray="3 3" />
                                            <XAxis dataKey="role" />
                                            <YAxis />
                                            <Tooltip />
                                            <Bar dataKey="demand" fill="#3b82f6" />
                                        </BarChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
};

                </AnimatePresence>
            </div>
        </div>
    );
};
