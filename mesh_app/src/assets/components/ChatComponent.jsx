import React, { useState, useEffect } from 'react';

const ChatComponent = () => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState(["הי", "אני חוזר עכשיו לבסיס"]);

  const sendMessage = async () => {
    setMessages([...messages, message])
    try {
      const response = await fetch('http://127.0.0.1:5000/send_message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: message,
        }),
      });
      if (response.ok) {
        console.log('Message sent successfully');
        setMessage(''); // Reset message input after sending
        fetchMessages(); // Fetch messages after sending
      } else {
        console.error('Failed to send message');
      }
    } catch (error) {
      console.error('Error:', error);
    }
    setMessage(''); // Reset message input after sending
  };

  const fetchMessages = async () => {
    console.log('on fetch messages')
    try {
      const response = await fetch('http://127.0.0.1:5000/get_messages');
      if (response.ok) {
        const data = await response.json();
        console.log(`data: ${data}`)
        setMessages(data);
      } else {
        console.error('Failed to fetch messages');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  useEffect(() => {
    fetchMessages(); // Fetch messages when component mounts
  }, []);

  return (
    <div className="shadow-lg rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-700">
        <h2 className="text-2xl font-semibold text-green-500">Chat</h2>
      </div>
      <div className="p-6 space-y-4 max-h-96 overflow-y-auto">
        {messages.map((msg, index) => (
          <div key={index} className="flex items-start">
            <div className="w-10 h-10 rounded-full bg-gray-600 flex-shrink-0">
              <span className="text-white text-lg font-bold">{index % 2 === 0 ? '#' : '&'}</span>
            </div>
            <div className="ml-4 bg-gray-800 text-green-500 rounded-lg p-4 shadow">
              <p>{msg}</p>
            </div>
          </div>
        ))}
      </div>
      <div className="px-6 py-4 border-t border-gray-700">
        <div className="flex items-center">
          <input
            className="flex-grow border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            type="text"
            placeholder="Type a message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
          <button 
            className="ml-4 bg-green-500 text-white px-4 py-2 rounded-lg flex items-center"
            onClick={sendMessage}
          >
            Send <span className="ml-2">&#10148;</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatComponent;
