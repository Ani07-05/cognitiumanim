﻿import React from 'react';

interface VideoPlayerProps {
  videoUrl: string;
  autoPlay?: boolean;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ videoUrl, autoPlay = false }) => (
  <div className="mt-4 bg-gray-800 rounded-lg overflow-hidden shadow-lg">
    <div className="relative pt-[56.25%]">
      <video 
        className="absolute top-0 left-0 w-full h-full rounded-lg"
        controls
        autoPlay={autoPlay}
        playsInline
        src={videoUrl}
      >
        Your browser does not support the video tag.
      </video>
    </div>
  </div>
);

export default VideoPlayer;
