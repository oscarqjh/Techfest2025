import { LinkPreview } from "@/components/ui/link-preview";
import WebResultCard from "./result-header-card";
import { forwardRef } from "react";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import AiInsights from "./ai-insights";

interface ResultSectionProps {
  data: any;
}

const ResultSection = forwardRef<HTMLDivElement, ResultSectionProps>(
  ({ data }, ref) => {
    return (
      <Card className="flex flex-col w-[72%] h-fit p-5 bg-transparent border-transparent">
        <div
          ref={ref}
          className="flex flex-col items-center justify-center w-full h-fit mb-[10%]"
        >
          <AiInsights data={data} />
          {/* <Separator className="w-[88%] h-px my-5" /> */}
          <WebResultCard
            weblink={data.parsed_web_results.parsed_web_results.weblink}
            domain={data.parsed_web_results.parsed_web_results.domain}
            title={data.parsed_web_results.parsed_web_results.title}
            content={data.parsed_web_results.parsed_web_results.content}
            image_urls={data.parsed_web_results.parsed_web_results.image_urls}
            date={data.parsed_web_results.parsed_web_results.date}
          />

          {data.web_research_results.web_research_results.map((item: any) => (
            <>
              {item.type === "image" ? (
                <img
                  src={item.src}
                  alt={item.alt}
                  className="w-[30%] h-auto place-items-center"
                />
              ) : (
                <div
                  key={item.id}
                  className="flex flex-col w-[90%] h-fit p-5  shadow-lg"
                >
                  {item.to_fact_check ? (
                    <LinkPreview
                      url=""
                      search_result={item.search_results}
                      fact_check={item.fact_check}
                      className="text-yellow-300 text-justify hover:cursor-pointer hover:text-yellow-500 transition-all"
                    >
                      {item.content}
                    </LinkPreview>
                  ) : (
                    <p className="text-zinc-300 text-justify">{item.content}</p>
                  )}
                </div>
              )}
            </>
          ))}
        </div>
      </Card>
    );
  }
);

export default ResultSection;
