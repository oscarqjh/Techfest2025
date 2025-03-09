import * as React from "react";

import { cn } from "@/lib/utils";

const HeroInput = React.forwardRef<
  HTMLInputElement,
  React.ComponentProps<"input">
>(({ className, type, ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        "flex h-12 w-full rounded-full border-4 border-zinc-950 bg-transparent px-3 py-1 text-primary-foreground shadow-sm transition-colors duration-500",
        "file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground",
        "placeholder:text-muted-foreground focus:border-zinc-200 focus:outline-none",
        "hover:border-zinc-700",
        "disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
        className
      )}
      ref={ref}
      {...props}
    />
  );
});
HeroInput.displayName = "Input";

export { HeroInput };
