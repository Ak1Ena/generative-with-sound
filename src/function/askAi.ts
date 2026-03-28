import { GoogleGenAI } from "@google/genai";
import { prompt } from "../config/prompt";
import {env} from '../config/env'

const ai = new GoogleGenAI({
  apiKey: env.BRIAN_CORE_API_KEY,
});
export async function askAi(message: string) {
     const stream = await ai.models.generateContentStream({
    model: "gemini-3.0-flash-preview",
    contents: message,
    config: {
      temperature: 0.7,
      systemInstruction: prompt,
    },
  });

  return stream;
}