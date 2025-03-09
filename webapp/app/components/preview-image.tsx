import { encode } from "qss";
import Image from "next/image";
import Link from "next/link";

export default function PreviewImage({
  url,
  width = 400,
  height = 200,
  quality = 50,
  layout = "fixed",
}) {
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
        layout={layout}
        priority={true}
        alt="image"
        className="rounded-lg"
      />
    </Link>
  );
}
