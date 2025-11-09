import React, { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";

interface AnalyticsEvent {
    event: string;
    userId?: string;
    data?: Record<string, any>;
    timestamp?: string;
}

interface AnalyticsTrackerProps {
    children: React.ReactNode;
}

class AnalyticsTracker {
    private static instance: AnalyticsTracker;
    private sessionId: string;
    private userId: string | undefined;
    private apiEndpoint: string;

    private constructor() {
        this.sessionId = this.generateSessionId();
        this.userId = this.getUserId();
        // Use a default endpoint for client-side or get from window object
        this.apiEndpoint = (window as any).APP_CONFIG?.apiEndpoint || "/analytics";
    }

    public static getInstance(): AnalyticsTracker {
        if (!AnalyticsTracker.instance) {
            AnalyticsTracker.instance = new AnalyticsTracker();
        }
        return AnalyticsTracker.instance;
    }

    private generateSessionId(): string {
        return "session_" + Date.now() + "_" + Math.random().toString(36).substr(2, 9);
    }

    private getUserId(): string | undefined {
        try {
            const stored = localStorage.getItem("career_navigator_user_id");
            if (stored) {
                return stored;
            }
            const newUserId = "user_" + Date.now() + "_" + Math.random().toString(36).substr(2, 9);
            localStorage.setItem("career_navigator_user_id", newUserId);
            return newUserId;
        } catch (error) {
            console.warn("Could not access localStorage:", error);
            return undefined;
        }
    }

    public async track(event: string, data?: Record<string, any>): Promise<void> {
        try {
            const eventData: AnalyticsEvent = {
                event,
                userId: this.userId,
                data: {
                    ...data,
                    sessionId: this.sessionId,
                    url: window.location.href,
                    userAgent: navigator.userAgent,
                    timestamp: new Date().toISOString()
                }
            };

            // Only send analytics in production or when explicitly enabled
            const isDevelopment = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
            if (isDevelopment && !(window as any).ENABLE_DEV_ANALYTICS) {
                console.log("Analytics (dev mode):", eventData);
                return;
            }

            await fetch(this.apiEndpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(eventData)
            });
        } catch (error) {
            console.warn("Analytics tracking failed:", error);
        }
    }

    public trackPageView(page: string): void {
        this.track("page_view", { page });
    }

    public trackUserAction(action: string, details?: Record<string, any>): void {
        this.track("user_action", { action, ...details });
    }

    public trackResumeAnalysis(analysisData: { matchScore: number; skillsFound: number; skillsMissing: number; analysisTime: number }): void {
        this.track("resume_analysis", analysisData);
    }

    public trackSocialShare(platform: string, content: string): void {
        this.track("social_share", { platform, content });
    }
}

// React component wrapper
export const AnalyticsProvider: React.FC<AnalyticsTrackerProps> = ({ children }) => {
    const tracker = useRef<AnalyticsTracker>();

    useEffect(() => {
        tracker.current = AnalyticsTracker.getInstance();

        // Track initial page load
        tracker.current.trackPageView(window.location.pathname);

        // Track page visibility changes
        const handleVisibilityChange = () => {
            if (document.visibilityState === "visible") {
                tracker.current?.trackUserAction("page_focus");
            } else {
                tracker.current?.trackUserAction("page_blur");
            }
        };

        document.addEventListener("visibilitychange", handleVisibilityChange);

        return () => {
            document.removeEventListener("visibilitychange", handleVisibilityChange);
        };
    }, []);

    return <>{children}</>;
};

// Export the tracker instance for use in other components
export const analytics = AnalyticsTracker.getInstance();

export default AnalyticsProvider;

// React hook for analytics
export const useAnalytics = () => {
    const location = useLocation();

    useEffect(() => {
        // Track page views
        analytics.trackPageView(location.pathname);
    }, [location]);

    useEffect(() => {
        // Track session start
        analytics.trackUserAction("session_started", {
            userAgent: navigator.userAgent,
            language: navigator.language,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            screenResolution: `${screen.width}x${screen.height}`,
            viewportSize: `${window.innerWidth}x${window.innerHeight}`
        });

        // Track performance metrics
        const trackPageLoad = () => {
            const navigation = performance.getEntriesByType("navigation")[0] as PerformanceNavigationTiming;
            if (navigation) {
                analytics.trackResumeAnalysis({
                    matchScore: 0,
                    skillsFound: 0,
                    skillsMissing: 0,
                    analysisTime: navigation.loadEventEnd - navigation.loadEventStart
                });
            }
        };

        if (document.readyState === "complete") {
            trackPageLoad();
        } else {
            window.addEventListener("load", trackPageLoad);
            return () => window.removeEventListener("load", trackPageLoad);
        }
    }, []);

    return {
        track: analytics.track.bind(analytics),
        trackPageView: analytics.trackPageView.bind(analytics),
        trackUserAction: analytics.trackUserAction.bind(analytics),
        trackResumeAnalysis: analytics.trackResumeAnalysis.bind(analytics),
        trackSocialShare: analytics.trackSocialShare.bind(analytics)
    };
};

// HOC for automatic analytics tracking
export const withAnalytics = <P extends object>(WrappedComponent: React.ComponentType<P>, eventName?: string) => {
    return (props: P) => {
        const analytics = useAnalytics();

        useEffect(() => {
            if (eventName) {
                analytics.track(eventName, { component: WrappedComponent.name });
            }
        }, [analytics]);

        return <WrappedComponent {...props} />;
    };
};

// Utility functions for common tracking scenarios
export const trackResumeUpload = (fileType: string, fileSize: number) => {
    analytics.trackResumeAnalysis({
        matchScore: 0,
        skillsFound: 0,
        skillsMissing: 0,
        analysisTime: Date.now()
    });
};

export const trackAnalysisStart = (analysisType: string) => {
    analytics.trackUserAction("analysis_started", {
        analysisType,
        timestamp: Date.now()
    });
};

export const trackAnalysisComplete = (analysisType: string, score: number, duration: number) => {
    analytics.trackResumeAnalysis({
        matchScore: score,
        skillsFound: 0,
        skillsMissing: 0,
        analysisTime: duration
    });
};

export const trackInterviewPrepUsage = (questionType: string, difficulty: string) => {
    analytics.trackUserAction("interview_prep_used", {
        questionType,
        difficulty,
        timestamp: Date.now()
    });
};

export const trackSocialShare = (platform: string, context: string) => {
    analytics.trackSocialShare(platform, context);
};

export const trackUserSuccess = (successType: string, metadata: Record<string, any> = {}) => {
    analytics.trackUserAction("user_success", {
        successType,
        ...metadata,
        timestamp: Date.now()
    });
};
