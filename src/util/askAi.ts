import { GoogleGenAI } from "@google/genai";
import { prompt } from "../config/prompt";
import {env} from '../config/env'

const ai = new GoogleGenAI({
  apiKey: env.BRIAN_CORE_API_KEY,
});
async function askAi(message: string) {
    const response = await ai.models.generateContent({
        model: "gemini-3.0-flash",
        contents: message,
        config:{
            temperature: 0.7,
            systemInstruction: prompt
        }
    });
    return response;
}