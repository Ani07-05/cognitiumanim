import React, { FormEvent } from 'react';
import { useState } from 'react';

interface Message {
  text: string;
  sender: 'user' | 'system';
}

interface ChatBoxProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
}

const ChatBox = ({ messages, onSendMessage }: ChatBoxProps) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  return (
    <div className="bg-gray-800 p-4 rounded-lg">
      <div className="h-64 overflow-y-auto mb-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-2 ${msg.sender === 'user' ? 'text-right' : 'text-left'}`}
          >
            <span
              className={`inline-block p-2 rounded-lg ${
                msg.sender === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-white'
              }`}
            >
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="flex">
        <input
          type="text"
          className="flex-1 bg-gray-700 text-white border border-gray-600 rounded-l-lg px-4 py-2 focus:outline-none focus:border-blue-500"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message here..."
        />
        <button
          type="submit"
          className="bg-white text-black px-4 py-2 rounded-r-lg hover:bg-gray-200 transition"
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatBox;