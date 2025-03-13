import { AnimatedCircularProgressBar } from "@/components/magicui/animated-circular-progress-bar";
import { Card, CardDescription, CardTitle } from "./ai-card";
import { BackgroundLines } from "@/components/ui/background-lines";

interface AiInsightsProps {
  data: any;
}

export default function AiInsights({ data }: AiInsightsProps) {
  return (
    <div className="text-zinc-300 text-justify">
      <Card className="relative w-[88%]">
        <BackgroundLines className="absolute inset-0 bg-transparent">
          <div></div>
        </BackgroundLines>
        <div className="flex">
          <div className="flex flex-col">
            <CardTitle className="cursor-default">AI Insights</CardTitle>
            <CardDescription className="mt-4">
              {JSON.parse(data.insights.raw.replace(/'/g, '"'))?.insights}
            </CardDescription>
          </div>
          <div className="flex flex-col items-center justify-center w-[20%] ml-14 cursor-default">
            <p className="mb-4 font-bold cursor-default">Article Score</p>
            <AnimatedCircularProgressBar
              max={100}
              min={0}
              value={
                JSON.parse(data.insights.raw.replace(/'/g, '"'))
                  ?.reliability_score
              }
              gaugePrimaryColor="rgb(79 70 229)"
              gaugeSecondaryColor="rgba(0, 0, 0, 0.1)"
            />
          </div>
        </div>
      </Card>
    </div>
  );
}
