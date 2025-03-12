import { AnimatedCircularProgressBar } from "@/components/magicui/animated-circular-progress-bar";
import Image from "next/image";
import { Card } from "./ai-card";
import { Button } from "@/components/ui/button";
import {
  ArrowBigDown,
  ArrowDown,
  ArrowDownToLineIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  WrenchIcon,
} from "lucide-react";
import { S } from "@upstash/redis/zmscore-C3G81zLz";
import { Separator } from "@/components/ui/separator";
import { useState } from "react";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import SideScrollingImages from "./scrolling-img";

const shimmer = (w: number, h: number) => `
<svg width="${w}" height="${h}" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="g">
      <stop stop-color="#333" offset="20%" />
      <stop stop-color="#222" offset="50%" />
      <stop stop-color="#333" offset="70%" />
    </linearGradient>
  </defs>
  <rect width="${w}" height="${h}" fill="#333" />
  <rect id="r" width="${w}" height="${h}" fill="url(#g)" />
  <animate xlink:href="#r" attributeName="x" from="-${w}" to="${w}" dur="1s" repeatCount="indefinite"  />
</svg>`;

const toBase64 = (str: string) =>
  typeof window === "undefined"
    ? Buffer.from(str).toString("base64")
    : window.btoa(str);

interface ImageCardProps {
  item: any;
}

const ImageCard = ({ item }: ImageCardProps) => {
  const [expandHovered, setExpandHovered] = useState(false);
  const [expand, setExpand] = useState(false);
  const text = "Related Images";

  const handleClick = () => {
    console.log(item);
  };
  return (
    <Card className="relative w-[88%] mb-4">
      <div className="flex flex-col w-full h-fit">
        <div className="flex items-center justify-center w-full h-fit">
          <div className="flex flex-col w-[50%]">
            <img
              src={item.src}
              alt={item.alt}
              className="h-auto place-items-center rounded-md border-4 border-zinc-500"
            />
            <span className="break-all italic text-zinc-300 font-light text-xs mt-2">
              {"Source: " + item.src}
            </span>
          </div>

          {/* <div className="flex flex-col items-center justify-center w-[50%] ml-14 cursor-default text-zinc-300">
            <p className="mb-4 font-bold cursor-default">
              Alteration Confidence Score
            </p>
            <AnimatedCircularProgressBar
              max={100}
              min={0}
              value={60}
              gaugePrimaryColor="rgb(79 70 229)"
              gaugeSecondaryColor="rgba(0, 0, 0, 0.1)"
            />
          </div> */}
        </div>
        {/* <div className="flex flex-col w-full h-fit justify-start items-start mt-4">
          <Button
            className="px-0 text-zinc-300 hover:bg-zinc-300 transition-colors hover:bg-transparent hover:text-zinc-500"
            variant="ghost"
            onMouseOver={() => setExpandHovered(true)}
            onMouseLeave={() => setExpandHovered(false)}
            onClick={() => setExpand(!expand)}
          >
            {expand ? (
              <ChevronDownIcon size={24} className="" />
            ) : (
              <ChevronUpIcon size={24} className="" />
            )}
            <div className=" text-zinc-300 flex">
              {!expand && (
                <motion.span
                  initial={{ opacity: 0 }}
                  animate={expandHovered ? { opacity: 0.8 } : {}}
                  transition={{ duration: 0.3 }}
                >
                  {text}
                </motion.span>
              )}
            </div>
          </Button>
          {!expand && (
            <Separator
              className={cn(
                "w-full transition-colors",
                expandHovered && "bg-slate-500"
              )}
            />
          )}
          {expand && (
            <div className="flex flex-col w-full h-fit">
              <p className="ml-2 font-bold text-zinc-300 text-justify mt-4">
                Related Images
              </p>
              <div className="relative"></div>
            </div>
          )}
        </div> */}
      </div>
    </Card>
  );
};

export default ImageCard;
