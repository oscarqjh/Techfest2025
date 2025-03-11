import { Inter } from "@next/font/google";
import LocalFont from "@next/font/local";
import { Metadata } from "next";
import { Analytics } from "./components/analytics";
import "../global.css";

export const metadata: Metadata = {
  title: {
    default: "https://techfest2025-red.vercel.app/",
    template: "%s | techfest2025-red.vercel.app/",
  },
  description: "Fake news detection using AI agents",
  openGraph: {
    title: "Techfest 2025 project",
    description: "Fake news detection using AI agents",
    url: "/https://techfest2025-red.vercel.app",
    siteName: "techfest2025",
    // images: [
    //   {
    //     url: "https://chronark.com/og.png",
    //     width: 1920,
    //     height: 1080,
    //   },
    // ],
    locale: "en-US",
    type: "website",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  // twitter: {
  //   title: "Chronark",
  //   card: "summary_large_image",
  // },
  icons: {
    shortcut: "/favicon-32x32.png",
  },
};
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

const calSans = LocalFont({
  src: "../public/fonts/CalSans-SemiBold.ttf",
  variable: "--font-calsans",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={[inter.variable, calSans.variable].join(" ")}>
      <body
        className={`bg-black ${
          process.env.NODE_ENV === "development" ? "debug-screens" : undefined
        }`}
      >
        {children}
      </body>
    </html>
  );
}
