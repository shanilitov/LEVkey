import React from 'react';

const ChatComponent = () => {
  return (
    <div className="shadow-lg rounded-lg overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-700">
        <h2 className="text-2xl font-semibold text-green-500">Chat</h2>
      </div>
      <div className="p-6 space-y-4 max-h-96 overflow-y-auto">
        {/* Incoming Message */}
        <div className="flex items-start">
          <div className="w-10 h-10 rounded-full bg-gray-600 flex-shrink-0">
            <span className="text-white text-lg font-bold">#</span>
          </div>
          <div className="ml-4 bg-gray-800 text-green-500 rounded-lg p-4 shadow">
            <p>Hello! How are you?</p>
          </div>
        </div>
        {/* Outgoing Message */}
        <div className="flex items-start justify-end">
          <div className="mr-4 bg-green-500 text-white rounded-lg p-4 shadow">
            <p>I'm good, thanks! How about you?</p>
          </div>
          <div className="w-10 h-10 rounded-full bg-gray-600 flex-shrink-0">
            <span className="text-white text-lg font-bold">&</span>
          </div>
        </div>
        {/* Incoming Message */}
        <div className="flex items-start">
          <div className="w-10 h-10 rounded-full bg-gray-600 flex-shrink-0">
            <span className="text-white text-lg font-bold">#</span>
          </div>
          <div className="ml-4 bg-gray-800 text-green-500 rounded-lg p-4 shadow">
            <p>I'm great, thanks for asking!</p>
          </div>
        </div>
      </div>
      <div className="px-6 py-4 border-t border-gray-700">
        <div className="flex items-center">
          <input
            className="flex-grow border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            type="text"
            placeholder="Type a message..."
          />
          <button className="ml-4 bg-green-500 text-white px-4 py-2 rounded-lg flex items-center">
            Send <span className="ml-2">&#10148;</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatComponent;
