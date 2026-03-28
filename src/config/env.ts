import 'dotenv/config'
export const BRIAN_CORE_API_KEY = process.env.BRIAN_CORE_API_KEY || ''
export const VOICE_CORE_API_KEY = process.env.VOICE_CORE_API_KEY || ''
export const VOICE_ID = process.env.VOICE_ID || ''
export const MODEL = process.env.MODEL || 'gemini-2.5-flash'
export const VOICE_MODEL = process.env.VOICE_MODEL || "eleven_v3"