import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const generateAnimation = async (topic: string) => {
  try {
    const response = await axios.post(`${API_URL}/visualize`, { topic });
    return response.data;
  } catch (error: any) {
    throw new Error(error.response?.data?.error || 'API request failed');
  }
};