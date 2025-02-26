﻿import React, { FormEvent } from 'react';
import VideoPlayer from './VideoPlayer';

interface Message {
  text: string;
  sender: 'user' | 'system';
  videoUrl?: string;
}

interface ChatBoxProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
}

const ChatBox: React.FC<ChatBoxProps> = ({ messages, onSendMessage }) => {
  const [input, setInput] = React.useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  return (
    <div className="bg-gray-800 p-4 rounded-lg">
      <div className="h-[400px] overflow-y-auto mb-4 space-y-4">
        {messages.map((msg, index) => (
          <div key={index} className="flex flex-col gap-2">
            <div className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <span
                className={`inline-block p-2 rounded-lg ${
                  msg.sender === 'user' ? 'bg-blue-600' : 'bg-gray-700'
                } text-white max-w-[80%]`}
              >
                {msg.text}
              </span>
            </div>
            {msg.videoUrl && (
              <div className="w-full max-w-3xl mx-auto">
                <VideoPlayer videoUrl={msg.videoUrl} autoPlay={false} />
              </div>
            )}
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 bg-gray-700 text-white border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500"
          placeholder="Type your message here..."
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatBox;
