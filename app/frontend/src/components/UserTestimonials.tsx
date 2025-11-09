import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { StarIcon, ChatBubbleLeftIcon } from "@heroicons/react/24/solid";
import { ShimmerEffect } from "./ui/ShimmerEffect";
import { Star } from "lucide-react";

interface Testimonial {
    id: number;
    name: string;
    role: string;
    company: string;
    avatar: string;
    rating: number;
    text: string;
    outcome: string;
    beforeAfter?: {
        before: string;
        after: string;
    };
}

const testimonials: Testimonial[] = [
    {
        id: 1,
        name: "Sarah Chen",
        role: "Software Engineer",
        company: "Google",
        avatar: "👩🏻‍💻",
        rating: 5,
        text: "AI Career Navigator transformed my job search! The resume analysis helped me identify key gaps, and I landed my dream job at Google within 2 months.",
        outcome: "Landed job at Google",
        beforeAfter: {
            before: "45% match rate",
            after: "94% match rate"
        }
    },
    {
        id: 2,
        name: "Marcus Johnson",
        role: "Data Scientist",
        company: "Microsoft",
        avatar: "👨🏿‍💼",
        rating: 5,
        text: "The AI interview prep was incredible! It generated questions I hadn't thought of and helped me practice until I felt confident. Got the offer!",
        outcome: "Salary increased by 40%",
        beforeAfter: {
            before: "65K salary",
            after: "91K salary"
        }
    },
    {
        id: 3,
        name: "Priya Sharma",
        role: "Full Stack Developer",
        company: "Startup",
        avatar: "👩🏽‍💻",
        rating: 5,
        text: "The skill gap analysis was eye-opening. It showed me exactly which technologies to learn for my target roles. Now I'm a senior developer!",
        outcome: "Promoted to Senior",
        beforeAfter: {
            before: "Junior Developer",
            after: "Senior Developer"
        }
    },
    {
        id: 4,
        name: "Alex Rodriguez",
        role: "DevOps Engineer",
        company: "Amazon",
        avatar: "👨🏻‍💻",
        rating: 5,
        text: "This platform is a game-changer! The career roadmap feature helped me plan my transition from web dev to DevOps. Highly recommend!",
        outcome: "Successful career pivot",
        beforeAfter: {
            before: "Frontend Developer",
            after: "DevOps Engineer"
        }
    },
    {
        id: 5,
        name: "Emily Wang",
        role: "Product Manager",
        company: "Netflix",
        avatar: "👩🏻‍💼",
        rating: 5,
        text: "The AI insights were spot-on! It helped me tailor my resume for PM roles and practice behavioral questions. Netflix here I come! 🚀",
        outcome: "PM role at Netflix",
        beforeAfter: {
            before: "Marketing Analyst",
            after: "Product Manager"
        }
    }
];

export const UserTestimonials: React.FC = () => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const timer = setTimeout(() => setIsLoading(false), 1000);
        return () => clearTimeout(timer);
    }, []);

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentIndex(prev => (prev + 1) % testimonials.length);
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    const handleDotClick = (index: number) => {
        setCurrentIndex(index);
    };

    if (isLoading) {
        return (
            <div className="max-w-4xl mx-auto p-6">
                <ShimmerEffect className="h-8 w-64 mx-auto mb-8 rounded-lg bg-gray-200" />
                <ShimmerEffect className="h-64 w-full rounded-2xl bg-gray-200" />
            </div>
        );
    }

    return (
        <motion.div className="max-w-4xl mx-auto p-6" initial={{ opacity: 0, y: 50 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
            <div className="text-center mb-12">
                <motion.h2
                    className="text-4xl font-bold text-secondary-900 mb-4"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    Success Stories
                </motion.h2>
                <motion.p className="text-xl text-secondary-600" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
                    Join thousands who've transformed their careers with AI Career Navigator
                </motion.p>
            </div>

            {/* Main Testimonial Display */}
            <div className="relative h-80 mb-8">
                <AnimatePresence mode="wait">
                    <motion.div
                        key={currentIndex}
                        className="absolute inset-0 bg-gradient-to-br from-white via-primary-50 to-accent-50 rounded-3xl border border-white/50 shadow-2xl overflow-hidden"
                        initial={{ opacity: 0, x: 100, rotateY: 15 }}
                        animate={{ opacity: 1, x: 0, rotateY: 0 }}
                        exit={{ opacity: 0, x: -100, rotateY: -15 }}
                        transition={{ duration: 0.6, ease: "easeInOut" }}
                    >
                        <div className="relative h-full p-8 flex flex-col justify-center">
                            {/* Quote Icon */}
                            <ChatBubbleLeftIcon className="absolute top-6 left-6 h-8 w-8 text-primary-300" />

                            {/* Avatar and Info */}
                            <div className="flex items-center mb-6">
                                <div className="w-16 h-16 bg-gradient-to-r from-primary-600 to-accent-500 rounded-full flex items-center justify-center text-2xl mr-4 shadow-lg">
                                    {testimonials[currentIndex].avatar}
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-secondary-900">{testimonials[currentIndex].name}</h3>
                                    <p className="text-secondary-600">
                                        {testimonials[currentIndex].role} at {testimonials[currentIndex].company}
                                    </p>
                                    <div className="flex items-center mt-1">
                                        {[...Array(testimonials[currentIndex].rating)].map((_, i) => (
                                            <StarIcon key={i} className="h-4 w-4 text-yellow-400" />
                                        ))}
                                    </div>
                                </div>
                            </div>

                            {/* Testimonial Text */}
                            <blockquote className="text-lg text-secondary-700 leading-relaxed mb-6 italic">"{testimonials[currentIndex].text}"</blockquote>

                            {/* Before/After Stats */}
                            {testimonials[currentIndex].beforeAfter && (
                                <div className="grid grid-cols-2 gap-4 mb-4">
                                    <div className="text-center p-3 bg-red-50 rounded-xl border border-red-200">
                                        <p className="text-xs text-red-600 font-semibold mb-1">BEFORE</p>
                                        <p className="text-sm font-bold text-red-700">{testimonials[currentIndex].beforeAfter?.before}</p>
                                    </div>
                                    <div className="text-center p-3 bg-green-50 rounded-xl border border-green-200">
                                        <p className="text-xs text-green-600 font-semibold mb-1">AFTER</p>
                                        <p className="text-sm font-bold text-green-700">{testimonials[currentIndex].beforeAfter?.after}</p>
                                    </div>
                                </div>
                            )}

                            {/* Outcome Badge */}
                            <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-full text-sm font-semibold shadow-lg">
                                <span className="mr-2">🎉</span>
                                {testimonials[currentIndex].outcome}
                            </div>
                        </div>
                    </motion.div>
                </AnimatePresence>
            </div>

            {/* Navigation Dots */}
            <div className="flex justify-center space-x-3 mb-8">
                {testimonials.map((_, index) => (
                    <motion.button
                        key={index}
                        onClick={() => handleDotClick(index)}
                        className={`w-3 h-3 rounded-full transition-all duration-300 ${
                            index === currentIndex ? "bg-primary-600 scale-125" : "bg-secondary-300 hover:bg-primary-400"
                        }`}
                        whileHover={{ scale: 1.2 }}
                        whileTap={{ scale: 0.9 }}
                    />
                ))}
            </div>

            {/* Statistics */}
            <motion.div
                className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-12"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6, duration: 0.8 }}
            >
                {[
                    { number: "10,000+", label: "Resumes Analyzed", icon: "📄" },
                    { number: "85%", label: "Success Rate", icon: "🎯" },
                    { number: "40%", label: "Avg Salary Increase", icon: "💰" },
                    { number: "4.9/5", label: "User Rating", icon: "⭐" }
                ].map((stat, index) => (
                    <motion.div
                        key={index}
                        className="text-center p-6 bg-white/60 backdrop-blur-sm rounded-2xl border border-white/50 shadow-lg"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.8 + index * 0.1 }}
                        whileHover={{ y: -5, scale: 1.05 }}
                    >
                        <div className="text-3xl mb-2">{stat.icon}</div>
                        <div className="text-2xl font-bold text-primary-600 mb-1">{stat.number}</div>
                        <div className="text-sm text-secondary-600 font-medium">{stat.label}</div>
                    </motion.div>
                ))}
            </motion.div>

            {/* Call to Action */}
            <motion.div className="text-center mt-12" initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 1, duration: 0.8 }}>
                <p className="text-lg text-secondary-600 mb-6">Ready to join our successful community?</p>
                <motion.button
                    className="px-8 py-4 bg-gradient-to-r from-primary-600 to-accent-500 text-white font-bold rounded-2xl shadow-2xl hover:shadow-primary-500/25 transition-all duration-300"
                    whileHover={{ scale: 1.05, y: -2 }}
                    whileTap={{ scale: 0.95 }}
                >
                    Start Your Success Story 🚀
                </motion.button>
            </motion.div>
        </motion.div>
    );
};

export default UserTestimonials;
