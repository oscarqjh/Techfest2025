import React from "react";

interface ResultAiOpinionProps {
  misinformationScore: number;
  explanation: string;
}

const ResultAiOpinionCard: React.FC<ResultAiOpinionProps> = ({
  misinformationScore,
  explanation,
}) => {
  const scoreColor =
    misinformationScore < 0.3
      ? "bg-green-500"
      : misinformationScore < 0.7
      ? "bg-yellow-500"
      : "bg-red-500";

  return (
    <div className="w-full p-4 bg-white dark:bg-zinc-800 shadow-lg rounded-xl">
      <h2 className="text-lg font-semibold text-zinc-900 dark:text-white">
        AI's Opinion
      </h2>
      <div className="mt-2">
        <div className="flex justify-between text-sm font-medium text-zinc-700 dark:text-zinc-300">
          <span>Misinformation Score</span>
          <span>{(misinformationScore * 100).toFixed(0)}%</span>
        </div>
        <div className="w-full h-2 mt-1 bg-zinc-200 dark:bg-zinc-600 rounded-full overflow-hidden">
          <div
            className={`h-full ${scoreColor}`}
            style={{ width: `${misinformationScore * 100}%` }}
          ></div>
        </div>
      </div>
      <p className="mt-3 text-sm text-zinc-700 dark:text-zinc-300">
        {explanation}
      </p>
    </div>
  );
};

export default ResultAiOpinionCard;
