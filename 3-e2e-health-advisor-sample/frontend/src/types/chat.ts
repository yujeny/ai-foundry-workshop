export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  response: string;
  disclaimer?: string;
  error?: string;
  message?: string;
}
