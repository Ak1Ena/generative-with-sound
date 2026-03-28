import { GoogleGenAI } from "@google/genai";
import { prompt } from "../config/prompt";
import {BRIAN_CORE_API_KEY, MODEL} from '../config/env'

const ai = new GoogleGenAI({
  apiKey: BRIAN_CORE_API_KEY,
});
export async function askAi(message: string) {
     const stream = await ai.models.generateContentStream({
    model: MODEL,
    contents: message,
    config: {
      temperature: 0.7,
      systemInstruction: prompt,
    },
  });

  return stream;
}