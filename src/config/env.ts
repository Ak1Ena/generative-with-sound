function getEnv(name: string): string {
  const value = process.env[name];

  if (!value) {
    throw new Error(`❌ Missing env: ${name}`);
  }

  return value;
}
function getEnvNumber(name: string): number {
  const value = getEnv(name);
  const num = Number(value);

  if (isNaN(num)) {
    throw new Error(`❌ Env ${name} must be a number`);
  }

  return num;
}

export const env = {
  BRIAN_CORE_API_KEY: getEnv("BRIAN_CORE_API_KEY"),
  VOICE_CORE_API_KEY: getEnv("VOICE_CORE_API_KEY"),
    DB_NAME: getEnv("DB_NAME"),
  DB_PASSWORD: getEnv("DB_PASSWORD"),
  DB_HOST: getEnv("DB_HOST"),
  DB_PORT: getEnvNumber("DB_PORT"),
};