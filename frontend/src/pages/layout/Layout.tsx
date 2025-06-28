import React, { useState, useEffect, useRef, RefObject } from "react";
import { Outlet, NavLink, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import styles from "./Layout.module.css";
import { motion } from "framer-motion";
import { Toaster } from "react-hot-toast";
import { HomeIcon, ChartBarIcon, UserIcon, Cog6ToothIcon, Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";

import { useLogin } from "../../authConfig";

import { LoginButton } from "../../components/LoginButton";
import { IconButton } from "@fluentui/react";
import { Github } from "../../components/Github";

// GitHub SVG will be inline

const Layout = () => {
    const { t } = useTranslation();
    const [menuOpen, setMenuOpen] = useState(false);
    const menuRef: RefObject<HTMLDivElement> = useRef(null);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const toggleMenu = () => {
        setMenuOpen(!menuOpen);
    };

    const handleClickOutside = (event: MouseEvent) => {
        if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
            setMenuOpen(false);
        }
    };

    useEffect(() => {
        if (menuOpen) {
            document.addEventListener("mousedown", handleClickOutside);
        } else {
            document.removeEventListener("mousedown", handleClickOutside);
        }
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [menuOpen]);

    const navItems = [
        { to: "/", icon: HomeIcon, label: "Home" },
        { to: "/qa", icon: ChartBarIcon, label: "Resume Analysis" },
        { to: "/chat", icon: UserIcon, label: "Career Chat" }
    ];

    return (
        <div className="flex flex-col min-h-screen bg-gradient-to-br from-secondary-50 to-primary-50">
            <Toaster
                position="top-right"
                toastOptions={{
                    duration: 4000,
                    style: {
                        background: "#fff",
                        color: "#1e293b",
                        border: "1px solid #e2e8f0",
                        borderRadius: "12px",
                        boxShadow: "0 10px 40px rgba(0, 0, 0, 0.1)"
                    },
                    success: {
                        iconTheme: {
                            primary: "#10b981",
                            secondary: "#fff"
                        }
                    },
                    error: {
                        iconTheme: {
                            primary: "#ef4444",
                            secondary: "#fff"
                        }
                    }
                }}
            />

            {/* Modern Navigation Header */}
            <header className="relative z-50">
                <nav className="glass backdrop-blur-md border-b border-white/20 sticky top-0 z-40">
                    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                        <div className="flex justify-between items-center h-20">
                            {/* Logo */}
                            <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="flex items-center space-x-3">
                                <Link to="/" className="flex items-center space-x-3 group">
                                    <div className="relative w-16 h-20 bg-gradient-to-r from-primary-600 to-accent-500 rounded-xl flex justify-center items-center shadow-lg group-hover:shadow-xl transition-all duration-300 overflow-visible z-10">
                                        {/* Floating emoji for logo */}
                                        <motion.div
                                            animate={{ y: [0, -15, 0] }}
                                            transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
                                            className="text-2xl absolute left-1/2 -translate-x-1/2"
                                        >
                                            🚀
                                        </motion.div>
                                    </div>
                                    <div className="absolute -inset-1 bg-gradient-to-r from-primary-600 to-accent-500 rounded-xl opacity-20 group-hover:opacity-30 blur-lg transition-all duration-300"></div>
                                    <div>
                                        <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-accent-500 bg-clip-text text-transparent">
                                            AI Career Navigator
                                        </h1>
                                        <p className="text-sm text-secondary-500 font-medium">Your Future Starts Here</p>
                                    </div>
                                </Link>
                            </motion.div>

                            {/* Desktop Navigation */}
                            <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="hidden md:flex items-center space-x-2">
                                {navItems.map((item, index) => (
                                    <motion.div
                                        key={item.to}
                                        initial={{ opacity: 0, y: -20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                    >
                                        <NavLink
                                            to={item.to}
                                            className={({ isActive }) =>
                                                `flex items-center space-x-2 px-6 py-3 rounded-xl font-medium transition-all duration-300 ${
                                                    isActive
                                                        ? "bg-primary-600 text-white shadow-lg"
                                                        : "text-secondary-600 hover:bg-white/50 hover:text-primary-600"
                                                }`
                                            }
                                        >
                                            <item.icon className="h-5 w-5" />
                                            <span>{item.label}</span>
                                        </NavLink>
                                    </motion.div>
                                ))}
                            </motion.div>

                            {/* User Actions */}
                            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="flex items-center space-x-4">
                                {/* Settings Button */}
                                <button className="hidden md:flex items-center space-x-2 px-4 py-2 text-secondary-600 hover:text-primary-600 transition-colors duration-300">
                                    <Cog6ToothIcon className="h-5 w-5" />
                                    <span className="font-medium">Settings</span>
                                </button>

                                {/* GitHub Link */}
                                <a
                                    href="https://github.com/azure-samples/azure-search-openai-demo"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="flex items-center space-x-2 px-4 py-2 bg-white/80 backdrop-blur-sm text-secondary-700 hover:text-primary-600 rounded-xl border border-secondary-200 hover:border-primary-300 transition-all duration-300"
                                >
                                    <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path
                                            fillRule="evenodd"
                                            d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z"
                                            clipRule="evenodd"
                                        />
                                    </svg>
                                    <span className="hidden lg:block font-medium">View on GitHub</span>
                                </a>

                                {/* Mobile Menu Button */}
                                <button
                                    onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                                    className="md:hidden p-2 text-secondary-600 hover:text-primary-600 transition-colors duration-300"
                                >
                                    {isMobileMenuOpen ? <XMarkIcon className="h-6 w-6" /> : <Bars3Icon className="h-6 w-6" />}
                                </button>
                            </motion.div>
                        </div>
                    </div>

                    {/* Mobile Menu */}
                    <motion.div
                        initial={false}
                        animate={{
                            height: isMobileMenuOpen ? "auto" : 0,
                            opacity: isMobileMenuOpen ? 1 : 0
                        }}
                        transition={{ duration: 0.3 }}
                        className="md:hidden overflow-hidden bg-white/90 backdrop-blur-md border-t border-secondary-200"
                    >
                        <div className="px-4 py-4 space-y-2">
                            {navItems.map(item => (
                                <NavLink
                                    key={item.to}
                                    to={item.to}
                                    onClick={() => setIsMobileMenuOpen(false)}
                                    className={({ isActive }) =>
                                        `flex items-center space-x-3 px-4 py-3 rounded-xl font-medium transition-all duration-300 ${
                                            isActive ? "bg-primary-600 text-white" : "text-secondary-600 hover:bg-primary-50 hover:text-primary-600"
                                        }`
                                    }
                                >
                                    <item.icon className="h-5 w-5" />
                                    <span>{item.label}</span>
                                </NavLink>
                            ))}
                            <div className="border-t border-secondary-200 pt-4 mt-4">
                                <button className="flex items-center space-x-3 px-4 py-3 w-full text-left text-secondary-600 hover:bg-primary-50 hover:text-primary-600 rounded-xl transition-all duration-300">
                                    <Cog6ToothIcon className="h-5 w-5" />
                                    <span className="font-medium">Settings</span>
                                </button>
                            </div>
                        </div>
                    </motion.div>
                </nav>
            </header>

            {/* Main Content */}
            <main className="relative flex-1 min-h-0">
                <Outlet />
            </main>

            {/* Footer */}
            <footer className="relative mt-20 border-t border-secondary-200 bg-white/50 backdrop-blur-md">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
                        {/* About */}
                        <div className="col-span-1 md:col-span-2">
                            <div className="flex items-center space-x-3 mb-4">
                                <div className="w-10 h-10 bg-gradient-to-r from-primary-600 to-accent-500 rounded-lg flex items-center justify-center">
                                    <span className="text-xl">🎯</span>
                                </div>
                                <h3 className="text-xl font-bold text-secondary-800">AI Career Navigator</h3>
                            </div>
                            <p className="text-secondary-600 mb-4 max-w-md">
                                Empowering students and professionals with AI-driven career insights, resume analysis, and personalized interview preparation.
                            </p>
                            <div className="flex space-x-4">
                                <span className="inline-flex items-center px-3 py-1 bg-success-100 text-success-700 rounded-full text-sm font-medium">
                                    ✨ Free to Use
                                </span>
                                <span className="inline-flex items-center px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium">
                                    🔬 AI-Powered
                                </span>
                            </div>
                        </div>

                        {/* Quick Links */}
                        <div>
                            <h4 className="font-semibold text-secondary-800 mb-4">Quick Links</h4>
                            <div className="space-y-2">
                                <Link to="/" className="block text-secondary-600 hover:text-primary-600 transition-colors duration-300">
                                    Home
                                </Link>
                                <Link to="/qa" className="block text-secondary-600 hover:text-primary-600 transition-colors duration-300">
                                    Resume Analysis
                                </Link>
                                <Link to="/chat" className="block text-secondary-600 hover:text-primary-600 transition-colors duration-300">
                                    Career Chat
                                </Link>
                            </div>
                        </div>

                        {/* Resources */}
                        <div>
                            <h4 className="font-semibold text-secondary-800 mb-4">Resources</h4>
                            <div className="space-y-2">
                                <a href="#" className="block text-secondary-600 hover:text-primary-600 transition-colors duration-300">
                                    Career Tips
                                </a>
                                <a href="#" className="block text-secondary-600 hover:text-primary-600 transition-colors duration-300">
                                    Interview Guide
                                </a>
                                <a href="#" className="block text-secondary-600 hover:text-primary-600 transition-colors duration-300">
                                    Resume Templates
                                </a>
                                <a
                                    href="https://github.com/azure-samples/azure-search-openai-demo"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="block text-secondary-600 hover:text-primary-600 transition-colors duration-300"
                                >
                                    GitHub Repository
                                </a>
                            </div>
                        </div>
                    </div>

                    <div className="border-t border-secondary-200 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
                        <p className="text-secondary-500 text-sm">© 2024 AI Career Navigator. Built with Azure OpenAI and Microsoft technologies.</p>
                        <div className="flex items-center space-x-6 mt-4 md:mt-0">
                            <span className="text-sm text-secondary-500">Powered by:</span>
                            <div className="flex items-center space-x-4">
                                <span className="text-sm font-medium text-primary-600">Azure OpenAI</span>
                                <span className="text-sm font-medium text-accent-600">React</span>
                                <span className="text-sm font-medium text-success-600">TypeScript</span>
                            </div>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Layout;
