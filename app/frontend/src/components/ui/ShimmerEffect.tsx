import React from "react";
import { motion } from "framer-motion";

interface ShimmerProps {
    className?: string;
    children?: React.ReactNode;
    delay?: number;
}

export const ShimmerEffect: React.FC<ShimmerProps> = ({ className = "", children, delay = 0 }) => {
    return (
        <motion.div className={`relative overflow-hidden ${className}`} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay, duration: 0.6 }}>
            {children}
            <motion.div
                className="absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/20 to-transparent"
                animate={{
                    translateX: ["100%", "100%", "-100%"]
                }}
                transition={{
                    duration: 2,
                    delay: delay + 0.5,
                    repeat: Infinity,
                    repeatDelay: 3,
                    ease: "easeInOut"
                }}
            />
        </motion.div>
    );
};

interface ShimmerCardProps {
    className?: string;
    animate?: boolean;
}

export const ShimmerCard: React.FC<ShimmerCardProps> = ({ className = "", animate = true }) => {
    return (
        <div className={`animate-pulse ${className}`}>
            <div className="bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 rounded-lg h-4 w-3/4 mb-3"></div>
            <div className="bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 rounded-lg h-3 w-1/2 mb-2"></div>
            <div className="bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 rounded-lg h-3 w-full mb-2"></div>
            <div className="bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 rounded-lg h-3 w-2/3"></div>

            {animate && (
                <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-transparent via-white/40 to-transparent"
                    animate={{
                        x: ["-100%", "100%"]
                    }}
                    transition={{
                        duration: 1.5,
                        repeat: Infinity,
                        ease: "easeInOut"
                    }}
                />
            )}
        </div>
    );
};

export default ShimmerEffect;
