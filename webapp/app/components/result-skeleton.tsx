"use client";

import { Skeleton } from "@/components/ui/skeleton";

export default function ResultSkeleton() {
  return (
    <div className="flex flex-col w-screen space-y-3 items-center mt-10 mb-10">
      <Skeleton className="h-[125px] w-[70%] rounded-xl" />
      <Skeleton className="h-[500px] w-[70%] rounded-xl" />
      <Skeleton className="h-[500px] w-[70%] rounded-xl" />
    </div>
  );
}
