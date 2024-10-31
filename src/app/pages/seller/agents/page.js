"use client";

import { useEffect, useState, useContext } from 'react';
import { AuthContext } from '../../authorization/AuthContext';
import { ReviewCard } from '../../../components/ReviewCard';
import axios from 'axios';

export default function ReviewRatingAgent() {
    const [agents, setAgents] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const { token } = useContext(AuthContext); // Get token from AuthContext
  
    // Function to fetch agents from API
    const fetchAgents = async () => {
      setIsLoading(true);
      setError('');
  
      try {
        const response = await axios.get('http://localhost:5000/api/users/search_agent', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          params: {
            first_name: '', // Adjust or add a search parameter here if needed
          },
        });
  
        setAgents(response.data.account_list); // Update agent list state
      } catch (error) {
        setError('Failed to fetch agents. Please try again.');
        console.error('Error fetching agents:', error);
      } finally {
        setIsLoading(false);
      }
    };
  
    // Fetch agents on component mount
    useEffect(() => {
      fetchAgents();
    }, [token]);
  
    return (
      <div className="min-h-screen bg-gray-100 p-6">
        <h1 className="text-3xl font-bold mb-6">Used Car Agents</h1>
  
        {/* Display error message */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
            {error}
          </div>
        )}
  
        {/* Loading Indicator */}
        {isLoading ? (
            <div className="flex justify-center items-center">
                <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-red-500"></div>
            </div>
            ) : (
          <div className="grid gap-4">
            {agents.length > 0 ? (
              agents.map((agent) => (
                <ReviewCard
                  key={agent.id} // Ensure unique key
                  name={`${agent.first_name} ${agent.last_name}`}
                  review={agent.review || 'No review available'} // Add default if no review is provided
                  rating={agent.rating || 0} // Add default rating
                />
              ))
            ) : (
              <p className="text-gray-500">No agents found.</p>
            )}
          </div>
        )}
      </div>
    );
  }