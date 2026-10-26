// Stands in for Deno's `npm:groq-sdk@0.26.0` under vitest (the package is not an App dependency); tests vi.mock it with behaviour.
type GroqCompletionResponse = {
  choices: Array<{ message?: { content?: string | null } }>;
  usage?: unknown;
};

class Groq {
  chat = {
    completions: {
      create: async (): Promise<GroqCompletionResponse> => ({
        choices: [{ message: { content: '' } }],
        usage: null,
      }),
    },
  };

  audio = {
    transcriptions: {
      create: async (): Promise<{ text: string }> => ({ text: '' }),
    },
  };

  constructor(_options?: unknown) {}
}

export default Groq;
