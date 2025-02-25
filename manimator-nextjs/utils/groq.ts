import axios from 'axios';

const GROQ_API_KEY = process.env.NEXT_PUBLIC_GROQ_API_KEY;
const GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions';

export const getReasoningResponse = async (message: string) => {
  try {
    const response = await axios.post(
      GROQ_API_URL,
      {
        model: 'deepseek-r1-distill-llama-70b',
        messages: [{ role: 'user', content: message }],
        temperature: 0.6,
        max_completion_tokens: 1024,
        top_p: 0.95,
        stream: false,
        reasoning_format: 'raw'
      },
      {
        headers: {
          Authorization: `Bearer ${GROQ_API_KEY}`,
          'Content-Type': 'application/json'
        }
      }
    );
    return response.data;
  } catch (error: any) {
    console.error('Error calling Groq API:', error);
    throw new Error('Groq API call failed');
  }
};