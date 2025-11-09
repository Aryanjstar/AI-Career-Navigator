import React from 'react';
import { motion } from 'framer-motion';

interface BentoCardProps {
  title: string;
  description: string;
  icon: string;
  className?: string;
}

const BentoCard: React.FC<BentoCardProps> = ({ title, description, icon, className }) => {
  return (
    <motion.div
      className={`bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-white/20 hover:bg-white/20 transition-all duration-300 ${className}`}
      whileHover={{ y: -5, scale: 1.02 }}
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-bold text-secondary-900 mb-2">{title}</h3>
      <p className="text-secondary-600">{description}</p>
    </motion.div>
  );
};

export default BentoCard; 