import React from "react";
import Image from "next/image"; // If using Next.js, otherwise replace with <img>
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
    <div className="max-w-md p-4 bg-white dark:bg-zinc-800 shadow-lg rounded-xl">
      {image_urls && image_urls.length > 0 && (
        <div className="w-full h-48 relative rounded-md overflow-hidden">
          <Image
            src={image_urls[0]}
            alt="Article image"
            layout="fill"
            objectFit="cover"
            className="rounded-md"
          />
        </div>
      )}
      <div className="mt-3">
        <a
          href={weblink}
          target="_blank"
          rel="noopener noreferrer"
          className="text-lg font-semibold text-blue-600 dark:text-blue-400 hover:underline"
        >
          {title}
        </a>
        <p className="mt-1 text-sm text-zinc-700 dark:text-zinc-300">
          {content.length > 250 ? content.slice(0, 250) + "..." : content}
        </p>
      </div>
      <div className="mt-3 flex justify-between items-center text-xs text-zinc-500 dark:text-zinc-400">
        <span>{domain}</span>
        {date && <span>{format(new Date(date), "MMMM d, yyyy")}</span>}
      </div>
    </div>
  );
};

export default WebResultCard;
