import { NextResponse } from "next/server";

export async function GET() {
  try {
    console.log("GET request");
    // Use different endpoints for development and production
    const API_BASE_URL =
      process.env.NODE_ENV === "development"
        ? "http://localhost:8000/get_data" // Dev endpoint
        : "https://techfest2025.onrender.com/get_data"; // Prod endpoint

    const response = await fetch(API_BASE_URL, {
      method: "GET",
      next: { revalidate: 0 },
      headers: {
        "Cache-Control": "no-store",
        Authorization: `Bearer ${process.env.RENDER_API_KEY}`,
      },
    });

    const data = await response.json();

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json(
      { message: "Internal Server Error", error: (error as Error).message },
      { status: 500 }
    );
  }
}
