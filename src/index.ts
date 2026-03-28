import readline from "readline";
import { initialize } from "./migrations/dataSource";
import { askAi } from "./function/askAi";
import { speak } from "./function/speak";

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

async function main() {
  await initialize();

  console.log("App started. Type something (or 'exit'):");

  rl.on("line", async (input) => {
    const message = input.trim();

    if (message === "exit") {
      console.log("Bye!");
      rl.close();
      process.exit(0);
    }

    try {
        const text = await askAi(message)
        for await (const chunk of text) {
          const text = chunk.text;
          if (!text) continue;
          await speak(text);
        }
    } catch (err) {
      console.error("Error:", err);
    }

    rl.prompt();
  });

  rl.prompt();
}

main();