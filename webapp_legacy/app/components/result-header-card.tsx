import React from "react";
import { format } from "date-fns"; // To format the date

interface ParsedWebResultProps {
  weblink: string;
  domain: string;
  title: string;
  content: string;
  image_urls?: string[];
  date?: string;
}

const WebResultCard: React.FC<ParsedWebResultProps> = ({
  weblink,
  domain,
  title,
  content,
  image_urls,
  date,
}) => {
  return (
    <div className="w-[90%] p-4 dark:bg-zinc-800 shadow-lg rounded-xl">
      <div className="mt-3">
        <h1 className="text-3xl font-bold text-zinc-200 text-justify">
          {title}
        </h1>
      </div>
      <div className="mt-3 flex justify-between items-center text-xs text-zinc-300 dark:text-zinc-400">
        <span>{domain}</span>
        {date && <span>{format(new Date(date), "MMMM d, yyyy")}</span>}
      </div>
    </div>
  );
};

export default WebResultCard;
