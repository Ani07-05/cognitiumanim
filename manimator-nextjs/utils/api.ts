﻿import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const generateAnimation = async (topic: string) => {
  try {
    const response = await axios.post(`${API_URL}/visualize`, { topic });
    // Return the full response data which includes request_id
    return {
      status: response.data.status,
      message: response.data.message,
      request_id: response.data.request_id
    };
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'API request failed');
  }
};
