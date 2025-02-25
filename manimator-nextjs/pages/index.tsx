import { useState, useEffect } from 'react';
import ChatBox from '../components/ChatBox';
import ProgressBar from '../components/ProgressBar';
import VideoPlayer from '../components/VideoPlayer';
import { generateAnimation } from '../utils/api';
import { getReasoningResponse } from '../utils/groq';
import io from 'socket.io-client';
import React from 'react';

const SOCKET_URL = 'http://localhost:5000';

export default function Home() {
  const [messages, setMessages] = useState([] as { text: string; sender: 'user' | 'system' }[]);
  const [progress, setProgress] = useState(0);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const socket = io(SOCKET_URL, { transports: ['websocket'] });

    socket.on('connect', () => {
      console.log('Connected to WebSocket server');
    });

    socket.on('progress', (data: { progress: number }) => {
      console.log('Progress update:', data);
      setProgress(data.progress);
    });

    socket.on('completed', (data: { videoUrl: string; topic: string }) => {
      console.log('Animation completed:', data);
      setVideoUrl(data.videoUrl);
      setProgress(100);
      setMessages((prev) => [
        ...prev,
        { text: `Animation for ${data.topic} completed!`, sender: 'system' },
        { text: `Video: [Click to Play](${data.videoUrl})`, sender: 'system' },
      ]);
    });

    socket.on('error', (data: { message: string }) => {
      console.error('Socket error:', data);
      setError(data.message);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleSendMessage = async (message: string) => {
    setMessages((prev) => [...prev, { text: message, sender: 'user' }]);
    setError(null);
    setVideoUrl(null); // Reset video on new message

    if (message.startsWith('@visualize')) {
      const topic = message.replace('@visualize', '').trim();
      if (topic) {
        try {
          await generateAnimation(topic);
          setMessages((prev) => [
            ...prev,
            { text: `Animation generation started for: "${topic}"`, sender: 'system' },
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
        {videoUrl && (
          <div className="mt-4">
            <VideoPlayer videoUrl={videoUrl} />
          </div>
        )}
      </div>
    </div>
  );
}