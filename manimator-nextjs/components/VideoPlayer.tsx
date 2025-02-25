import React from 'react';

interface VideoPlayerProps {
  videoUrl: string;
}

const VideoPlayer = ({ videoUrl }: VideoPlayerProps) => {
  return (
    <div className="mt-4">
      <video controls className="w-full rounded-lg" src={videoUrl} />
    </div>
  );
};

export default VideoPlayer;