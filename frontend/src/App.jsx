import { useState, useRef, useEffect } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: 'Hello! I am Tara, your AI Course Assistant. Ask me anything about the courses available on this platform!',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  const formatText = (text) => {
    // Basic formatting to convert bold text (**text**) and newlines to HTML
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br/>')
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!inputValue.trim()) return

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: inputValue.trim(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }

    setMessages((prev) => [...prev, userMsg])
    setInputValue('')
    setIsTyping(true)

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMsg.text }),
      })

      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`);
      }

      const data = await response.json()

      const botMsg = {
        id: Date.now() + 1,
        sender: 'bot',
        text: data.response || "I'm sorry, I couldn't process that.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }

      setMessages((prev) => [...prev, botMsg])
    } catch (error) {
      console.error("Error communicating with backend:", error)
      const errorMsg = {
        id: Date.now() + 1,
        sender: 'bot',
        text: "Sorry, I'm having trouble connecting to the server. Please check your network connection or try again later.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
      setMessages((prev) => [...prev, errorMsg])
    } finally {
      setIsTyping(false)
    }
  }

  return (
    <div className="app-container">
      <div className="chat-wrapper glass-panel">
        
        {/* Header */}
        <header className="chat-header">
          <div className="avatar">
            <i className="bi bi-robot"></i>
          </div>
          <div className="header-info">
            <h1>Tara AI</h1>
            <p><span className="status-dot"></span> Online and ready to help</p>
          </div>
        </header>

        {/* Chat Messages */}
        <div className="chat-messages">
          {messages.map((msg) => (
            <div key={msg.id} className={`message-group ${msg.sender}`}>
              <div className="message-bubble">
                {msg.sender === 'bot' ? (
                  <div 
                    className="bot-markdown"
                    dangerouslySetInnerHTML={{ __html: formatText(msg.text) }} 
                  />
                ) : (
                  <p>{msg.text}</p>
                )}
              </div>
              <span className="message-time">{msg.timestamp}</span>
            </div>
          ))}

          {isTyping && (
            <div className="message-group bot">
              <div className="message-bubble">
                <div className="typing-indicator">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <form onSubmit={handleSendMessage} className="chat-input-container">
          <div className="input-wrapper">
            <input
              type="text"
              className="chat-input"
              placeholder="Ask Tara about the courses..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={isTyping}
            />
            <button 
              type="submit" 
              className="send-button"
              disabled={!inputValue.trim() || isTyping}
            >
              <i className="bi bi-send-fill"></i>
            </button>
          </div>
        </form>

      </div>
    </div>
  )
}

export default App
