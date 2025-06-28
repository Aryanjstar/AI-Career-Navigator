import React, { useState, useEffect } from "react";
import { motion, useInView } from "framer-motion";

interface SplitTextProps {
    children: string;
    className?: string;
    delay?: number;
    duration?: number;
    variant?: "fade" | "slide" | "scale" | "rotate" | "blur";
}

export const SplitText: React.FC<SplitTextProps> = ({ children, className = "", delay = 0, duration = 0.05, variant = "fade" }) => {
    const [isVisible, setIsVisible] = useState(false);
    const ref = React.useRef(null);
    const isInView = useInView(ref, { once: true, margin: "-50px" });

    useEffect(() => {
        if (isInView) {
            setIsVisible(true);
        }
    }, [isInView]);

    const words = children.split(" ");

    const variants = {
        fade: {
            hidden: { opacity: 0, y: 20 },
            visible: { opacity: 1, y: 0 }
        },
        slide: {
            hidden: { opacity: 0, x: -20 },
            visible: { opacity: 1, x: 0 }
        },
        scale: {
            hidden: { opacity: 0, scale: 0.8 },
            visible: { opacity: 1, scale: 1 }
        },
        rotate: {
            hidden: { opacity: 0, rotateX: 90 },
            visible: { opacity: 1, rotateX: 0 }
        },
        blur: {
            hidden: { opacity: 0, filter: "blur(10px)" },
            visible: { opacity: 1, filter: "blur(0px)" }
        }
    };

    return (
        <div ref={ref} className={className}>
            {words.map((word, wordIndex) => (
                <span key={wordIndex} className="inline-block">
                    {word.split("").map((char, charIndex) => (
                        <motion.span
                            key={charIndex}
                            className="inline-block"
                            variants={variants[variant]}
                            initial="hidden"
                            animate={isVisible ? "visible" : "hidden"}
                            transition={{
                                duration: 0.6,
                                delay: delay + wordIndex * 0.1 + charIndex * duration,
                                ease: "easeOut"
                            }}
                        >
                            {char}
                        </motion.span>
                    ))}
                    {wordIndex < words.length - 1 && <span className="inline-block">&nbsp;</span>}
                </span>
            ))}
        </div>
    );
};

interface TypingTextProps {
    text: string;
    className?: string;
    speed?: number;
    showCursor?: boolean;
}

export const TypingText: React.FC<TypingTextProps> = ({ text, className = "", speed = 50, showCursor = true }) => {
    const [displayedText, setDisplayedText] = useState("");
    const [isComplete, setIsComplete] = useState(false);
    const ref = React.useRef(null);
    const isInView = useInView(ref, { once: true });

    useEffect(() => {
        if (!isInView) return;

        let currentIndex = 0;
        const timer = setInterval(() => {
            setDisplayedText(text.slice(0, currentIndex + 1));
            currentIndex++;

            if (currentIndex === text.length) {
                setIsComplete(true);
                clearInterval(timer);
            }
        }, speed);

        return () => clearInterval(timer);
    }, [isInView, text, speed]);

    return (
        <span ref={ref} className={className}>
            {displayedText}
            {showCursor && (
                <motion.span
                    className="inline-block w-0.5 h-6 bg-current ml-1"
                    animate={{ opacity: isComplete ? 0 : [1, 0] }}
                    transition={{
                        duration: 0.8,
                        repeat: isComplete ? 0 : Infinity,
                        repeatType: "reverse"
                    }}
                />
            )}
        </span>
    );
};

interface GradientTextProps {
    children: string;
    className?: string;
    gradient?: string;
    animate?: boolean;
}

export const GradientText: React.FC<GradientTextProps> = ({
    children,
    className = "",
    gradient = "from-primary-600 via-accent-500 to-primary-800",
    animate = true
}) => {
    return (
        <motion.span
            className={`bg-gradient-to-r ${gradient} bg-clip-text text-transparent ${className}`}
            {...(animate && {
                animate: {
                    backgroundPosition: ["0% 50%", "100% 50%", "0% 50%"]
                },
                transition: {
                    duration: 3,
                    repeat: Infinity,
                    ease: "easeInOut"
                },
                style: {
                    backgroundSize: "200% 200%"
                }
            })}
        >
            {children}
        </motion.span>
    );
};

export default SplitText;
