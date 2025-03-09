import { LinkPreview } from "@/components/ui/link-preview";
import WebResultCard from "./result-header-card";
import { forwardRef } from "react";

interface ResultSectionProps {
  data: any;
}

const ResultSection = forwardRef<HTMLDivElement, ResultSectionProps>(
  ({ data }, ref) => {
    return (
      <div
        ref={ref} // ✅ Now ref works!
        className="flex flex-col items-center justify-center w-screen h-fit mb-[10%]"
      >
        <WebResultCard
          weblink={data.parsed_web_results.parsed_web_results.weblink}
          domain={data.parsed_web_results.parsed_web_results.domain}
          title={data.parsed_web_results.parsed_web_results.title}
          content={data.parsed_web_results.parsed_web_results.content}
          image_urls={data.parsed_web_results.parsed_web_results.image_urls}
          date={data.parsed_web_results.parsed_web_results.date}
        />

        {data.web_research_results.web_research_results.map((item: any) => (
          <div
            key={item.id}
            className="flex flex-col w-[72%] h-fit p-5  shadow-lg"
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
        ))}
      </div>
    );
  }
);

export default ResultSection;
