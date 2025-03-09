import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json(); // Parse request body

    console.log(body);

<<<<<<< HEAD
    const response = await fetch("http://127.0.0.1:8000/api/v1/validate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
=======
    const response = await fetch(
      "https://techfest2025.onrender.com/sample_output",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${process.env.RENDER_API_KEY}`,
        },
        body: JSON.stringify(body),
      }
    );

    const data = await response.json();

    console.log(data);

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
    const response = await fetch(
      "https://techfest2025.onrender.com/sample_output",
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${process.env.RENDER_API_KEY}`,
        },
      }
    );
>>>>>>> staging

    const data = await response.json();

    console.log(data);

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    return NextResponse.json(
      { message: "Internal Server Error", error: (error as Error).message },
      { status: 500 }
    );
  }
}
