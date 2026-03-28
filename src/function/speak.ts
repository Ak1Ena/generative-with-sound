import { ElevenLabsClient, play } from "@elevenlabs/elevenlabs-js";
import { env } from "../config/env";

const elevenlabs = new ElevenLabsClient({apiKey: env.VOICE_CORE_API_KEY});

const prepare = async(message: string): Promise<Buffer> => {
    const audioStream = await elevenlabs.textToSpeech.convert(
        'JBFqnCBsd6RMkjVDRZzb',
         {
    text: message,
    modelId: 'eleven_v3',
    outputFormat: 'mp3_44100_128',
     voiceSettings: {
      stability: 0,
      similarityBoost: 1.0,
      useSpeakerBoost: true,
      speed: 1.0,
    },
  }
    )
    const chunks: Buffer[] = [];
    for await (const chunk of audioStream) {
    chunks.push(Buffer.from(chunk));
  }
  const content = Buffer.concat(chunks);
  return content
} 

export const speak = async (message: string) => {
    await prepare(message)
}