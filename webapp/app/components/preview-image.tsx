import { encode } from "qss";
import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { Spinner } from "@heroui/spinner";

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

interface PreviewImageProps {
  url: string;
  width?: number;
  height?: number;
  quality?: number;
  layout?: "fixed" | "intrinsic" | "responsive";
}

export default function PreviewImage({
  url,
  width = 400,
  height = 200,
  quality = 50,
}: PreviewImageProps) {
  const params = encode({
    url,
    screenshot: true,
    meta: false,
    embed: "screenshot.url",
    colorScheme: "dark",
    "viewport.isMobile": true,
    "viewport.deviceScaleFactor": 1,
    "viewport.width": width * 3,
    "viewport.height": height * 3,
  });
  const src = `https://api.microlink.io/?${params}`;

  return (
    <Link
      href={url}
      className="block p-1 bg-white border-4 border-neutral-700 shadow rounded-xl hover:border-neutral-200 dark:hover:border-neutral-800 transition-colors"
    >
      <Image
        src={src}
        width={width}
        height={height}
        quality={quality}
        priority={true}
        placeholder={`data:image/svg+xml;base64,${toBase64(shimmer(400, 200))}`}
        alt="image"
        className="rounded-lg"
      />
    </Link>
  );
}
