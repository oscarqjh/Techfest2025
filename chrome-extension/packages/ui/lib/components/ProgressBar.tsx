import React from 'react';
import './AnimatedCircularProgressBar.css'; // Make sure to import the CSS

interface ProgressBarProps {
  progress: number;
  size?: number;
  strokeWidth?: number;
}

export const AnimatedCircularProgressBar = ({ progress, size = 100, strokeWidth = 10 }: ProgressBarProps) => {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;

  const dashoffset = circumference - (progress / 100) * circumference;

  return (
    <div className="circular-progress-bar" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="circular-progress-bar-svg">
        <circle
          className="circular-progress-bar-background"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
        />
        <circle
          className="circular-progress-bar-foreground"
          cx={size / 2}
          cy={size / 2}
          r={radius}
          strokeWidth={strokeWidth}
          style={{
            strokeDasharray: circumference,
            strokeDashoffset: dashoffset,
          }}
        />
      </svg>
      <div className="circular-progress-bar-text">
        <span>{`${progress}%`}</span>
      </div>
    </div>
  );
};
