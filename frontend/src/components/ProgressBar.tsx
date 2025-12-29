/**
 * Progress Bar Component
 * Reusable progress visualization
 */
import React from 'react';

interface ProgressBarProps {
    percentage: number;
    height?: string;
    showLabel?: boolean;
    colorClass?: string;
}

export default function ProgressBar({
    percentage,
    height = 'h-2',
    showLabel = false,
    colorClass = 'bg-primary-500'
}: ProgressBarProps) {
    const clampedPercentage = Math.min(Math.max(percentage, 0), 100);

    return (
        <div className="w-full">
            <div className={`w-full bg-gray-700 rounded-full overflow-hidden ${height}`}>
                <div
                    className={`${colorClass} ${height} rounded-full transition-all duration-500 ease-out`}
                    style={{ width: `${clampedPercentage}%` }}
                />
            </div>
            {showLabel && (
                <p className="text-xs text-gray-400 mt-1 text-right">
                    {clampedPercentage.toFixed(0)}% Complete
                </p>
            )}
        </div>
    );
}
