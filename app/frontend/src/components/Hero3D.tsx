import React, { useRef, useMemo, useState, useEffect, Suspense, lazy } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Text, Float, Sphere, MeshDistortMaterial, OrbitControls } from "@react-three/drei";
import { motion, useInView, useAnimation } from "framer-motion";
import * as THREE from "three";
import { SplitText, TypingText, GradientText } from "./ui/SplitText";
import { ShimmerEffect } from "./ui/ShimmerEffect";
import { UserTestimonials } from "./UserTestimonials";
import { SocialShare } from "./SocialShare";
import { useAnalytics } from "./AnalyticsTracker";

// Lazy load heavy components
const LazyBentoCard = lazy(() => import("./ui/BentoCard"));

// 3D Brain Component
function Brain() {
    const meshRef = useRef<THREE.Mesh>(null);

    useFrame(state => {
        if (meshRef.current) {
            meshRef.current.rotation.x = state.clock.elapsedTime * 0.2;
            meshRef.current.rotation.y = state.clock.elapsedTime * 0.3;
        }
    });

    return (
        <Float speed={1.5} rotationIntensity={1} floatIntensity={2}>
            <Sphere ref={meshRef} args={[1, 100, 200]} scale={1.5}>
                <MeshDistortMaterial color="#3b82f6" attach="material" distort={0.3} speed={1.5} roughness={0} metalness={0.8} />
            </Sphere>
        </Float>
    );
}

// Floating Particles
function Particles() {
    const points = useRef<THREE.Points>(null);

    const particlesPosition = useMemo(() => {
        const positions = new Float32Array(500 * 3);
        for (let i = 0; i < 500; i++) {
            positions[i * 3] = (Math.random() - 0.5) * 10;
            positions[i * 3 + 1] = (Math.random() - 0.5) * 10;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 10;
        }
        return positions;
    }, []);

    useFrame(({ clock }) => {
        if (points.current) {
            points.current.rotation.x = clock.elapsedTime * 0.05;
            points.current.rotation.y = clock.elapsedTime * 0.075;
        }
    });

    return (
        <points ref={points}>
            <bufferGeometry>
                <bufferAttribute attach="attributes-position" count={particlesPosition.length / 3} array={particlesPosition} itemSize={3} />
            </bufferGeometry>
            <pointsMaterial size={0.015} color="#60a5fa" sizeAttenuation transparent opacity={0.8} />
        </points>
    );
}

// 3D Text Component
function AnimatedText() {
    return (
        <Float speed={2} rotationIntensity={0.5} floatIntensity={1}>
            <Text font="/fonts/Inter-Bold.woff" fontSize={0.8} color="#1e40af" anchorX="center" anchorY="middle" position={[0, 2, 0]}>
                AI Career Navigator
            </Text>
            <Text font="/fonts/Inter-Regular.woff" fontSize={0.3} color="#64748b" anchorX="center" anchorY="middle" position={[0, 1.2, 0]}>
                Your One-Stop Solution
            </Text>
        </Float>
    );
}

// Stats Counter Component with useInView hook
const StatsCounter: React.FC<{ value: number; label: string; suffix?: string }> = ({ value, label, suffix = "" }) => {
    const [count, setCount] = useState(0);
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true });

    useEffect(() => {
        if (isInView) {
            const interval = setInterval(() => {
                setCount(prev => {
                    if (prev < value) {
                        return Math.min(prev + Math.ceil(value / 50), value);
                    }
                    clearInterval(interval);
                    return value;
                });
            }, 50);
        }
    }, [isInView, value]);

    return (
        <motion.div
            ref={ref}
            className="text-center"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={isInView ? { opacity: 1, scale: 1 } : {}}
            transition={{ duration: 0.6 }}
        >
            <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-primary-600 to-accent-500 bg-clip-text text-transparent">
                {count}
                {suffix}
            </div>
            <div className="text-sm text-secondary-600 font-medium">{label}</div>
        </motion.div>
    );
};

// Bento Grid Item Component
const BentoGridItem: React.FC<{
    className?: string;
    title: string;
    description: string;
    icon: string;
    gradient: string;
    children?: React.ReactNode;
}> = ({ className, title, description, icon, gradient, children }) => {
    const ref = useRef(null);
    const isInView = useInView(ref, { once: true, margin: "-100px" });
    const controls = useAnimation();

    useEffect(() => {
        if (isInView) {
            controls.start("visible");
        }
    }, [isInView, controls]);

    return (
        <motion.div
            ref={ref}
            className={`relative group rounded-3xl border border-white/20 bg-white/10 backdrop-blur-md p-6 hover:bg-white/20 transition-all duration-500 ${className}`}
            initial="hidden"
            animate={controls}
            variants={{
                hidden: { opacity: 0, y: 50, scale: 0.95 },
                visible: { opacity: 1, y: 0, scale: 1 }
            }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            whileHover={{ y: -5, scale: 1.02 }}
        >
            <div className={`absolute inset-0 rounded-3xl bg-gradient-to-br ${gradient} opacity-0 group-hover:opacity-10 transition-opacity duration-500`} />

            <div className="relative z-10">
                <div className="text-4xl mb-4">{icon}</div>
                <h3 className="text-xl font-bold text-secondary-900 mb-2">{title}</h3>
                <p className="text-secondary-600 text-sm leading-relaxed">{description}</p>
                {children}
            </div>
        </motion.div>
    );
};

// Main Hero Component
export const Hero3D: React.FC = () => {
    const [isLoaded, setIsLoaded] = useState(false);
    const [showTestimonials, setShowTestimonials] = useState(false);
    const [showSocialShare, setShowSocialShare] = useState(false);
    const heroRef = useRef(null);
    const isHeroInView = useInView(heroRef, { once: true });
    const analytics = useAnalytics();

    useEffect(() => {
        const timer = setTimeout(() => setIsLoaded(true), 1000);
        return () => clearTimeout(timer);
    }, []);

    useEffect(() => {
        analytics.trackUserAction("feature_usage", { feature: "hero_3d", action: "page_load" });
    }, [analytics]);

    return (
        <div className="relative min-h-screen w-full overflow-hidden bg-gradient-to-br from-primary-50 via-white to-accent-50">
            {/* 3D Canvas */}
            <div className="absolute inset-0 opacity-80">
                <Suspense fallback={<div className="bg-gradient-to-br from-primary-50 to-accent-50 h-full" />}>
                    <Canvas camera={{ position: [0, 0, 5], fov: 60 }} style={{ background: "transparent" }}>
                        <ambientLight intensity={0.6} />
                        <pointLight position={[10, 10, 10]} intensity={1} />
                        <spotLight position={[-10, -10, -10]} angle={0.15} penumbra={1} intensity={0.5} />

                        <Brain />
                        <Particles />
                        <AnimatedText />

                        <OrbitControls enableZoom={false} enablePan={false} enableRotate={true} autoRotate={true} autoRotateSpeed={0.5} />
                    </Canvas>
                </Suspense>
            </div>

            {/* Hero Content */}
            <div ref={heroRef} className="relative z-10 pt-20 pb-32">
                <div className="container mx-auto px-6">
                    {/* Main Hero Section */}
                    <motion.div
                        className="text-center mb-32"
                        initial={{ opacity: 0, y: 50 }}
                        animate={isHeroInView ? { opacity: 1, y: 0 } : {}}
                        transition={{ duration: 1, delay: 0.5 }}
                    >
                        <motion.div
                            className="inline-block px-6 py-2 mb-8 bg-gradient-to-r from-primary-100 to-accent-100 rounded-full border border-primary-200"
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={isHeroInView ? { opacity: 1, scale: 1 } : {}}
                            transition={{ duration: 0.8, delay: 0.7 }}
                        >
                            <span className="text-primary-700 font-semibold text-sm">🚀 Your Career Transformation Starts Here</span>
                        </motion.div>

                        <SplitText
                            variant="fade"
                            delay={0.9}
                            className="text-5xl md:text-7xl font-bold leading-tight mb-6 bg-gradient-to-r from-primary-600 via-accent-500 to-primary-800 bg-clip-text text-transparent"
                        >
                            Your One-Stop Solution for Career Success
                        </SplitText>

                        <motion.p
                            className="text-xl md:text-2xl text-secondary-600 mb-12 max-w-4xl mx-auto leading-relaxed"
                            initial={{ opacity: 0, y: 30 }}
                            animate={isHeroInView ? { opacity: 1, y: 0 } : {}}
                            transition={{ duration: 1, delay: 1.1 }}
                        >
                            Transform your career with <span className="font-semibold text-primary-600">AI-powered resume analysis</span>,
                            <span className="font-semibold text-accent-600"> skill gap identification</span>, and
                            <span className="font-semibold text-primary-600"> personalized interview preparation</span> — all in one intelligent platform
                        </motion.p>

                        <motion.div
                            className="flex flex-col sm:flex-row gap-6 justify-center items-center mb-16"
                            initial={{ opacity: 0, y: 30 }}
                            animate={isHeroInView ? { opacity: 1, y: 0 } : {}}
                            transition={{ duration: 1, delay: 1.3 }}
                        >
                            <motion.button
                                className="px-10 py-4 bg-gradient-to-r from-primary-600 to-accent-500 text-white font-semibold rounded-2xl shadow-2xl hover:shadow-primary-500/25 transform transition-all duration-300 group"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => {
                                    analytics.trackUserAction("cta_clicked", { button: "start_analysis", location: "hero" });
                                    analytics.trackUserAction("lead_generation", { source: "hero_cta" });
                                }}
                            >
                                <span className="flex items-center gap-2">
                                    Start Free Analysis
                                    <span className="group-hover:translate-x-1 transition-transform">🚀</span>
                                </span>
                            </motion.button>

                            <motion.button
                                className="px-10 py-4 bg-white/80 backdrop-blur-md text-primary-700 font-semibold rounded-2xl border border-primary-200 hover:bg-white/90 transform transition-all duration-300 group"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                            >
                                <span className="flex items-center gap-2">
                                    Watch Demo
                                    <span className="group-hover:scale-110 transition-transform">▶️</span>
                                </span>
                            </motion.button>
                        </motion.div>

                        {/* Stats Section */}
                        <motion.div
                            className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-3xl mx-auto"
                            initial={{ opacity: 0, y: 30 }}
                            animate={isHeroInView ? { opacity: 1, y: 0 } : {}}
                            transition={{ duration: 1, delay: 1.5 }}
                        >
                            <StatsCounter value={95} label="Match Accuracy" suffix="%" />
                            <StatsCounter value={10000} label="Resumes Analyzed" suffix="+" />
                            <StatsCounter value={500} label="Interview Questions" suffix="+" />
                            <StatsCounter value={99} label="User Satisfaction" suffix="%" />
                        </motion.div>
                    </motion.div>

                    {/* Bento Grid Section */}
                    <motion.div
                        className="max-w-7xl mx-auto"
                        initial={{ opacity: 0 }}
                        animate={isLoaded ? { opacity: 1 } : {}}
                        transition={{ duration: 1, delay: 2 }}
                    >
                        <div className="text-center mb-16">
                            <h2 className="text-4xl font-bold text-secondary-900 mb-4">Everything You Need to Succeed</h2>
                            <p className="text-xl text-secondary-600">Comprehensive career tools powered by cutting-edge AI technology</p>
                        </div>

                        {/* Bento Grid Layout */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 auto-rows-[200px]">
                            {/* Large Feature Cards */}
                            <BentoGridItem
                                className="lg:col-span-2 lg:row-span-2"
                                title="AI Resume Analysis"
                                description="Get instant, detailed feedback on your resume with our advanced AI that analyzes content, format, and keyword optimization"
                                icon="🎯"
                                gradient="from-blue-500 to-indigo-600"
                            >
                                <div className="mt-4 p-4 bg-white/20 rounded-xl">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="text-sm font-medium">Match Score</span>
                                        <span className="text-lg font-bold text-primary-600">87%</span>
                                    </div>
                                    <div className="w-full bg-white/30 rounded-full h-2">
                                        <motion.div
                                            className="bg-gradient-to-r from-primary-500 to-accent-500 h-2 rounded-full"
                                            initial={{ width: 0 }}
                                            animate={{ width: "87%" }}
                                            transition={{ duration: 2, delay: 3 }}
                                        />
                                    </div>
                                </div>
                            </BentoGridItem>

                            <BentoGridItem
                                className="md:col-span-1"
                                title="Skill Gap Analysis"
                                description="Identify missing skills and get personalized learning paths"
                                icon="📊"
                                gradient="from-green-500 to-emerald-600"
                            />

                            <BentoGridItem
                                className="md:col-span-1"
                                title="Interview Prep"
                                description="Practice with AI-generated questions tailored to your role"
                                icon="🎭"
                                gradient="from-purple-500 to-violet-600"
                            />

                            <BentoGridItem
                                className="lg:col-span-2"
                                title="Career Insights Dashboard"
                                description="Track your progress, analyze trends, and make data-driven career decisions"
                                icon="📈"
                                gradient="from-orange-500 to-red-600"
                            >
                                <div className="mt-4 grid grid-cols-3 gap-2">
                                    {["Skills", "Growth", "Salary"].map((metric, i) => (
                                        <div key={metric} className="text-center p-2 bg-white/20 rounded-lg">
                                            <div className="text-lg font-bold text-primary-600">{["+15", "↗️", "$85K"][i]}</div>
                                            <div className="text-xs text-secondary-600">{metric}</div>
                                        </div>
                                    ))}
                                </div>
                            </BentoGridItem>

                            <BentoGridItem
                                className="md:col-span-1"
                                title="Salary Insights"
                                description="Get accurate salary estimates based on your skills and market data"
                                icon="💰"
                                gradient="from-yellow-500 to-orange-600"
                            />

                            <BentoGridItem
                                className="md:col-span-1"
                                title="ATS Optimization"
                                description="Ensure your resume passes Applicant Tracking Systems"
                                icon="🤖"
                                gradient="from-cyan-500 to-blue-600"
                            />

                            <BentoGridItem
                                className="lg:col-span-3"
                                title="AI Career Roadmap"
                                description="Get a personalized career path with milestone tracking, skill recommendations, and industry insights tailored to your goals"
                                icon="🗺️"
                                gradient="from-indigo-500 to-purple-600"
                            >
                                <div className="mt-4 flex items-center gap-4 overflow-x-auto">
                                    {["Junior Dev", "Mid-Level", "Senior Dev", "Tech Lead", "Architect"].map((stage, i) => (
                                        <div key={stage} className="flex-shrink-0 text-center">
                                            <div className={`w-3 h-3 rounded-full mx-auto mb-1 ${i <= 2 ? "bg-primary-500" : "bg-white/30"}`} />
                                            <div className="text-xs text-secondary-600 whitespace-nowrap">{stage}</div>
                                        </div>
                                    ))}
                                </div>
                            </BentoGridItem>

                            <BentoGridItem
                                className="md:col-span-1"
                                title="Community Insights"
                                description="Learn from anonymized trends and success patterns"
                                icon="👥"
                                gradient="from-pink-500 to-rose-600"
                            />
                        </div>
                    </motion.div>

                    {/* Level 4 Features: User Testimonials */}
                    <motion.div
                        className="mt-32"
                        initial={{ opacity: 0, y: 50 }}
                        animate={isLoaded ? { opacity: 1, y: 0 } : {}}
                        transition={{ duration: 1, delay: 2.5 }}
                    >
                        <Suspense fallback={<ShimmerEffect className="h-96 w-full rounded-2xl bg-gray-200 mx-auto" />}>
                            <UserTestimonials />
                        </Suspense>
                    </motion.div>

                    {/* Level 4 Features: Social Sharing */}
                    <motion.div
                        className="mt-24 max-w-2xl mx-auto"
                        initial={{ opacity: 0, y: 50 }}
                        animate={isLoaded ? { opacity: 1, y: 0 } : {}}
                        transition={{ duration: 1, delay: 3 }}
                    >
                        <Suspense fallback={<ShimmerEffect className="h-64 w-full rounded-2xl bg-gray-200" />}>
                            <SocialShare />
                        </Suspense>
                    </motion.div>

                    {/* CTA Section with Viral Mechanics */}
                    <motion.div
                        className="text-center mt-32"
                        initial={{ opacity: 0, y: 50 }}
                        animate={isLoaded ? { opacity: 1, y: 0 } : {}}
                        transition={{ duration: 1, delay: 3.5 }}
                    >
                        <SplitText variant="scale" delay={3.5} className="text-3xl font-bold text-secondary-900 mb-6">
                            Ready to Transform Your Career?
                        </SplitText>

                        <TypingText
                            text="Join thousands of professionals who've already accelerated their careers with our AI-powered platform"
                            className="text-lg text-secondary-600 mb-8 max-w-2xl mx-auto block"
                            speed={30}
                        />

                        <motion.div className="space-y-4">
                            <motion.button
                                className="px-12 py-5 bg-gradient-to-r from-primary-600 to-accent-500 text-white font-bold text-lg rounded-2xl shadow-2xl hover:shadow-primary-500/25 transform transition-all duration-300 block mx-auto"
                                whileHover={{ scale: 1.05 }}
                                whileTap={{ scale: 0.95 }}
                                onClick={() => {
                                    analytics.trackUserAction("final_cta_clicked", { location: "bottom" });
                                    analytics.trackUserAction("user_converted", { step: "final_cta" });
                                }}
                            >
                                Get Started Free Today 🚀
                            </motion.button>

                            <motion.p className="text-sm text-secondary-500" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 4 }}>
                                ✨ <strong>Limited Time:</strong> First 1000 users get lifetime premium features!
                            </motion.p>
                        </motion.div>
                    </motion.div>

                    {/* Real-time User Activity (Level 4) */}
                    <motion.div
                        className="mt-16 max-w-md mx-auto"
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={isLoaded ? { opacity: 1, scale: 1 } : {}}
                        transition={{ duration: 0.8, delay: 4 }}
                    >
                        <div className="bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-2xl p-4">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                                    <span className="text-sm font-medium text-green-700">
                                        🔥 <strong>{Math.floor(Math.random() * 50) + 20}</strong> people analyzing resumes right now
                                    </span>
                                </div>
                            </div>
                            <div className="mt-2 text-xs text-green-600">
                                <span className="inline-block w-2 h-2 bg-green-400 rounded-full mr-2 animate-ping"></span>
                                Someone just got hired at Microsoft! 🎉
                            </div>
                        </div>
                    </motion.div>
                </div>
            </div>
        </div>
    );
};
 