import Link from "next/link";
import React from "react";
import Particles from "./components/particles";
import { PlaceholdersAndVanishInput } from "@/components/ui/placeholders-and-vanish-input";
import ResultSkeleton from "./components/result-skeleton";
import { ScrollProgress } from "@/components/magicui/scroll-progress";
import ResultSection from "./components/result-section";

const placeholders = [
  "Enter your URL here",
  "https://www.straitstimes.com/",
  "https://www.channelnewsasia.com/",
  "https://www.todayonline.com/",
];

export default function Home() {
  const [url, setUrl] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState("");
  const [result, setResult] = React.useState("");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("/api/validate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      console.log(data);
      if (response.ok) {
        setResult(data.answer);
      } else {
        setError(data.error);
      }
    } catch (error) {
      setError("An error occurred, please try again later.");
    } finally {
      // setLoading(false);
      setTimeout(() => {
        setLoading(false);
      }, 5000);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center w-screen min-h-screen h-fit overflow-x-hidden bg-gradient-to-tl from-black via-zinc-600/20 to-black">
      <div className="overflow-x-hidden hidden w-screen h-px animate-glow md:block animate-fade-left bg-gradient-to-r from-zinc-300/0 via-zinc-300/50 to-zinc-300/0" />
      <Particles
        className="absolute inset-0 -z-10 animate-fade-in"
        quantity={100}
      />
      <div className="flex items-center justify-center mt-[10%]">
        <h1 className="py-3.5 px-0.5 z-10 text-4xl text-transparent duration-3000 bg-black cursor-default text-edge-outline animate-title font-display sm:text-6xl md:text-9xl whitespace-nowrap bg-clip-text">
          <div className="flex items-center justify-center mr-10">
            <span>Are</span>
          </div>
        </h1>
        <h1 className="py-3.5 px-0.5 z-10 text-4xl text-transparent duration-3000 bg-white cursor-default text-edge-outline animate-title font-display sm:text-6xl md:text-9xl whitespace-nowrap bg-clip-text">
          <div className="flex items-center justify-center mr-10">
            <span>U</span>
          </div>
        </h1>
        <h1 className="py-3.5 px-0.5 z-10 text-4xl text-transparent duration-3000 bg-white cursor-default text-edge-outline animate-title font-display sm:text-6xl md:text-9xl whitespace-nowrap bg-clip-text">
          <div className="flex items-center justify-center">
            <span>R</span>
          </div>
        </h1>
        <h1 className="py-3.5 px-0.5 z-10 text-4xl text-transparent duration-3000 bg-black cursor-default text-edge-outline animate-title font-display sm:text-6xl md:text-9xl whitespace-nowrap bg-clip-text">
          <div className="flex items-center justify-center">
            <span>ea</span>
          </div>
        </h1>
        <h1 className="py-3.5 px-0.5 z-10 text-4xl text-transparent duration-3000 bg-white cursor-default text-edge-outline animate-title font-display sm:text-6xl md:text-9xl whitespace-nowrap bg-clip-text">
          <div className="flex items-center justify-center">
            <span>L?</span>
          </div>
        </h1>
      </div>

      <div className="hidden w-screen h-px animate-glow md:block animate-fade-right bg-gradient-to-r from-zinc-300/0 via-zinc-300/50 to-zinc-300/0" />
      <div className="w-[40%] my-16 text-center animate-fade-in">
        <div className="h-[7rem] flex flex-col justify-center  items-center px-4">
          <PlaceholdersAndVanishInput
            placeholders={placeholders}
            onChange={(e) => setUrl(e.target.value)}
            onSubmit={handleSubmit}
            isLoading={loading}
          />
        </div>
      </div>

      {/** Result skeleton*/}
      {loading && <ResultSkeleton />}
      {result !== "" && !loading && <ResultSection data={result} />}
    </div>
  );
}
