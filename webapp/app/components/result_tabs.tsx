import { useState } from "react";
import PreviewImage from "./preview-image";
import { AnimatedCircularProgressBar } from "@/components/magicui/animated-circular-progress-bar";

interface SearchResultsTabsProps {
  search_results: any;
}

const SearchResultsTabs = ({ search_results }: SearchResultsTabsProps) => {
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <div className="w-full mx-auto">
      {/* Tabs */}
      <div className="flex border-b border-gray-300 dark:border-gray-600">
        {search_results?.map((result: any, index: any) => (
          <button
            key={index}
            className={`p-2 flex-1 text-sm font-semibold focus:outline-none transition-colors duration-200
              ${
                activeIndex === index
                  ? "border-b-2 border-zinc-500 text-zinc-500"
                  : "text-gray-500 hover:text-gray-700"
              }`}
            onClick={() => setActiveIndex(index)}
          >
            Related source {index + 1}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="p-4 w-full border h-[300px] overflow-auto border-gray-300 dark:border-gray-600 rounded-lg mt-2 bg-white dark:bg-gray-900">
        <div className="flex justify-start items-center w-full h-fit rounded-xl overflow-hidden">
          {search_results && (
            <>
              <PreviewImage url={search_results[activeIndex]?.url} />
              <div className="flex flex-col items-center justify-center ml-10">
                <p className="text-lg text-center mb-2">Relavence score</p>
                <AnimatedCircularProgressBar
                  max={100}
                  min={0}
                  value={search_results[activeIndex]?.score * 100}
                  gaugePrimaryColor="rgb(79 70 229)"
                  gaugeSecondaryColor="rgba(0, 0, 0, 0.1)"
                />
              </div>
            </>
          )}
        </div>
        <div className="p-2 w-full">
          <div className="text-sm font-bold">
            {search_results[activeIndex]?.title}
          </div>
          <div className="text-sm text-justify mt-2 text-neutral-600 dark:text-neutral-400">
            {search_results[activeIndex]?.content}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchResultsTabs;
