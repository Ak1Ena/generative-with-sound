import { ElevenLabsClient, play } from "@elevenlabs/elevenlabs-js";
import { VOICE_CORE_API_KEY, VOICE_ID, VOICE_MODEL } from "../config/env";

const elevenlabs = new ElevenLabsClient({apiKey: VOICE_CORE_API_KEY});
export const speak = async (message: string) => {
  const audioStream = await elevenlabs.textToSpeech.convert(
    VOICE_ID,
    {
      text: message,
      modelId: VOICE_MODEL,
      outputFormat: "mp3_44100_128",
      voiceSettings: {
        stability: 0,
        similarityBoost: 1.0,
        useSpeakerBoost: true,
        speed: 1.0,
      },
    }
  );

  await play(audioStream); // ✅ ถูกต้อง
  console.log(message);
};