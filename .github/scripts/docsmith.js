import fs from "fs";
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_AI_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash-latest" });

const generatedReadme = fs.existsSync("README.generated.md")
  ? fs.readFileSync("README.generated.md", "utf-8")
  : "";

const prompt = `
You are DocSmith, the M3TAL Infrastructure Architect.

Task:
Polish the README for the M3TAL Stack (m3tal-stack).

Rules:
- Professional, technical tone.
- Emphasize standardization: /mnt paths, shared bridge network, and Traefik routing.
- Explain its role as the foundation of the M3TAL runtime.
- Keep it concise.

RAW README:
${generatedReadme}
`;

async function run() {
  const result = await model.generateContent(prompt);
  fs.writeFileSync("README.md", result.response.text());
  console.log("README polished by DocSmith for M3TAL Stack.");
}

run();
