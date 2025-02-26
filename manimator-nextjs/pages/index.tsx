﻿﻿﻿﻿﻿﻿﻿import { useState, useEffect } from 'react';
import ChatBox from '../components/ChatBox';
import ProgressBar from '../components/ProgressBar';
import { generateAnimation } from '../utils/api';
import { getReasoningResponse } from '../utils/groq';
import io from 'socket.io-client';
import React from 'react';

const SOCKET_URL = 'http://127.0.0.1:5000';

export default function Home() {
  interface Message {
    text: string;
    sender: 'user' | 'system';
    videoUrl?: string;
  }

  const [messages, setMessages] = useState<Message[]>([{
    text: "Welcome! Enter @visualize followed by a topic (e.g. '@visualize bst') to generate an educational animation.",
    sender: 'system'
  }]);
  
  const [progress, setProgress] = useState(0);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentRequestId, setCurrentRequestId] = useState<string | null>(null);

  useEffect(() => {
    const socket = io(SOCKET_URL, { transports: ['websocket'] });

    socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    socket.on('progress', (data: { progress: number; request_id: string }) => {
      console.log('Progress update:', data);
      if (data.request_id === currentRequestId) {
        setProgress(data.progress);
      }
    });

    socket.on('completed', (data: { videoUrl: string; topic: string; request_id: string }) => {
      console.log('Animation completed:', data);
      if (data.request_id === currentRequestId) {
        setVideoUrl(data.videoUrl);
        setProgress(100);
        setMessages((prev) => [
          ...prev,
          { text: `Animation for ${data.topic} completed!`, sender: 'system', videoUrl: data.videoUrl },
        ]);
        setCurrentRequestId(null); // Reset request ID
      }
    });

    socket.on('error', (data: { message: string; request_id: string }) => {
      console.error('Socket error:', data);
      if (data.request_id === currentRequestId) {
        setError(data.message);
        setCurrentRequestId(null); // Reset request ID
      }
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleSendMessage = async (message: string) => {
    setMessages((prev) => [...prev, { text: message, sender: 'user' }]);
    setError(null);
    setVideoUrl(null);

    if (message.startsWith('@visualize')) {
      const topic = message.replace('@visualize', '').trim();
      if (topic) {
        try {
          const response = await generateAnimation(topic);
          setCurrentRequestId(response.request_id);
          setMessages((prev) => [
            ...prev,
            { text: `Animation generation started for: "${topic}"`, sender: 'system' }
          ]);
        } catch (err: any) {
          console.error('API error:', err);
          setError('Failed to generate animation: ' + err.message);
        }
      } else {
        setError('Please specify a topic for visualization.');
      }
    } else {
      try {
        const response = await getReasoningResponse(message);
        const answer = response.choices[0].message.content;
        setMessages((prev) => [...prev, { text: answer, sender: 'system' }]);
      } catch (error: any) {
        console.error('Groq API error:', error);
        setError('Failed to get reasoning response.');
      }
    }
  };

  return (
    <div className="min-h-screen bg-black text-white p-4">
      <div className="max-w-4xl mx-auto bg-gray-900 shadow-lg rounded-lg p-6">
        <h1 className="text-3xl font-bold mb-6 text-center">Manimator</h1>
        {error && (
          <div className="bg-red-600 text-white p-3 rounded mb-4">{error}</div>
        )}
        <ChatBox onSendMessage={handleSendMessage} messages={messages} />
        {progress > 0 && progress < 100 && <ProgressBar progress={progress} />}
      </div>
    </div>
  );
}
