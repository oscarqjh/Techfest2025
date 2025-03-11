import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json(); // Parse request body
    console.log("POST request");
    console.log(body);

    // Use different endpoints for development and production
    const API_BASE_URL =
      process.env.NODE_ENV === "development"
        ? "http://localhost:8000/analyse_credibility" // Dev endpoint
        : "https://techfest2025.onrender.com/analyse_credibility"; // Prod endpoint

    const response = await fetch(API_BASE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${process.env.RENDER_API_KEY}`,
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    console.log("hi");

    console.log(data.parsed_web_results);

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json(
      { message: "Internal Server Error", error: (error as Error).message },
      { status: 500 }
    );
  }
}

export async function GET() {
  try {
    console.log("GET request");
    // Use different endpoints for development and production
    const API_BASE_URL =
      process.env.NODE_ENV === "development"
        ? "http://localhost:8000/sample_output" // Dev endpoint
        : "https://techfest2025.onrender.com/sample_output"; // Prod endpoint

    const response = await fetch(API_BASE_URL, {
      method: "GET",
      headers: {
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
