"use client";

import { useRef } from "react";

const images = [
  "/images/image1.jpg",
  "/images/image2.jpg",
  "/images/image3.jpg",
  "/images/image4.jpg",
];

export default function SideScrollingImages() {
  const scrollRef = useRef<HTMLDivElement>(null);

  const handleWheelScroll = (event: React.WheelEvent) => {
    if (scrollRef.current) {
      event.preventDefault();
      scrollRef.current.scrollLeft += event.deltaY * 2; // Adjust speed
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto overflow-hidden scrollbar-hide">
      {/* Scrollable container */}
      <div
        ref={scrollRef}
        onWheel={handleWheelScroll}
        className="flex space-x-4 overflow-x-auto scroll-smooth scrollbar-hide snap-x snap-mandatory"
      >
        {images.map((src, index) => (
          <div key={index} className="snap-start flex-shrink-0">
            <img
              src={src}
              alt={`Image ${index + 1}`}
              className="w-72 h-48 rounded-lg object-cover"
            />
          </div>
        ))}
      </div>
    </div>
  );
}
