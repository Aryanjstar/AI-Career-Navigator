import React, { useState } from "react";
import { motion } from "framer-motion";
import { ShareIcon, ClipboardDocumentIcon, CheckIcon } from "@heroicons/react/24/outline";
import toast from "react-hot-toast";

interface SocialShareProps {
    url?: string;
    title?: string;
    description?: string;
    hashtags?: string[];
}

export const SocialShare: React.FC<SocialShareProps> = ({
    url = window.location.href,
    title = "I just analyzed my resume with AI Career Navigator! 🚀",
    description = "Transform your career with AI-powered resume analysis, skill gap identification, and interview prep. Join thousands who've accelerated their careers!",
    hashtags = ["AICareer", "ResumeAnalysis", "CareerGrowth", "TechJobs"]
}) => {
    const [copied, setCopied] = useState(false);

    const shareData = {
        title,
        text: description,
        url
    };

    const encodedUrl = encodeURIComponent(url);
    const encodedTitle = encodeURIComponent(title);
    const encodedDescription = encodeURIComponent(description);
    const hashtagString = hashtags.map(tag => `%23${tag}`).join("%20");

    const socialPlatforms = [
        {
            name: "Twitter",
            icon: "🐦",
            url: `https://twitter.com/intent/tweet?text=${encodedTitle}&url=${encodedUrl}&hashtags=${hashtags.join(",")}`
        },
        {
            name: "LinkedIn",
            icon: "💼",
            url: `https://linkedin.com/sharing/share-offsite/?url=${encodedUrl}&summary=${encodedDescription}`
        },
        {
            name: "Facebook",
            icon: "📘",
            url: `https://facebook.com/sharer/sharer.php?u=${encodedUrl}&quote=${encodedTitle}`
        },
        {
            name: "WhatsApp",
            icon: "💬",
            url: `https://api.whatsapp.com/send?text=${encodedTitle}%20${encodedUrl}`
        },
        {
            name: "Telegram",
            icon: "✈️",
            url: `https://t.me/share/url?url=${encodedUrl}&text=${encodedTitle}`
        }
    ];

    const handleNativeShare = async () => {
        if (navigator.share) {
            try {
                await navigator.share(shareData);
                toast.success("Thanks for sharing! 🎉");
            } catch (error) {
                console.log("Share cancelled");
            }
        } else {
            handleCopyLink();
        }
    };

    const handleCopyLink = async () => {
        try {
            await navigator.clipboard.writeText(url);
            setCopied(true);
            toast.success("Link copied to clipboard! 📋");
            setTimeout(() => setCopied(false), 2000);
        } catch (error) {
            toast.error("Failed to copy link");
        }
    };

    const handleSocialShare = (platform: any) => {
        window.open(platform.url, "_blank", "noopener,noreferrer");
        toast.success(`Shared on ${platform.name}! 🚀`);
    };

    return (
        <motion.div
            className="bg-white/90 backdrop-blur-md rounded-2xl p-6 border border-white/20 shadow-xl"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-secondary-900 flex items-center gap-2">
                    <ShareIcon className="h-5 w-5 text-primary-600" />
                    Share Your Success
                </h3>
                <motion.button
                    onClick={handleNativeShare}
                    className="px-4 py-2 bg-gradient-to-r from-primary-600 to-accent-500 text-white rounded-xl font-medium hover:shadow-lg transition-all duration-300"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    Share Now
                </motion.button>
            </div>

            <p className="text-secondary-600 mb-6 text-sm">Help others discover AI Career Navigator and accelerate their careers too! 🌟</p>

            {/* Social Platform Buttons */}
            <div className="grid grid-cols-5 gap-3 mb-6">
                {socialPlatforms.map(platform => (
                    <motion.button
                        key={platform.name}
                        onClick={() => handleSocialShare(platform)}
                        className="flex flex-col items-center p-3 rounded-xl border border-secondary-200 hover:border-primary-300 hover:bg-primary-50 transition-all duration-300"
                        whileHover={{ scale: 1.05, y: -2 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <span className="text-2xl mb-1">{platform.icon}</span>
                        <span className="text-xs font-medium text-secondary-600">{platform.name}</span>
                    </motion.button>
                ))}
            </div>

            {/* Copy Link Button */}
            <div className="flex items-center gap-3">
                <div className="flex-1 px-3 py-2 bg-secondary-50 rounded-lg border border-secondary-200">
                    <p className="text-sm text-secondary-600 truncate">{url}</p>
                </div>
                <motion.button
                    onClick={handleCopyLink}
                    className="px-4 py-2 bg-white border border-secondary-200 rounded-lg hover:bg-secondary-50 transition-all duration-300 flex items-center gap-2"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                >
                    {copied ? <CheckIcon className="h-4 w-4 text-green-500" /> : <ClipboardDocumentIcon className="h-4 w-4 text-secondary-600" />}
                    <span className="text-sm font-medium text-secondary-700">{copied ? "Copied!" : "Copy"}</span>
                </motion.button>
            </div>

            {/* Viral Incentive */}
            <motion.div
                className="mt-4 p-3 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border border-green-200"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
            >
                <p className="text-sm text-green-700 font-medium">
                    🎁 <strong>Referral Bonus:</strong> Share with 3 friends and unlock premium AI interview simulator!
                </p>
            </motion.div>
        </motion.div>
    );
};

export default SocialShare;
