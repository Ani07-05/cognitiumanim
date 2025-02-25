"use client";
import React from 'react';

interface ProgressBarProps {
  progress: number;
}

const ProgressBar = ({ progress }: ProgressBarProps) => {
  return (
    <div className="w-full bg-gray-700 rounded-full h-4 mt-4">
      <div
        className="bg-green-500 h-4 rounded-full"
        style={{ width: `${progress}%`, transition: 'width 0.5s ease-in-out' }}
      ></div>
    </div>
  );
};

export default ProgressBar;