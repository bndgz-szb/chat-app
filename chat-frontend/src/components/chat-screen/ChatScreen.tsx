import Message from '@/components/chat-screen/Message';
import { ChatContext } from '@/contexts/ChatContext';
import { WebSocketContext } from '@/contexts/WebSocketContext';
import { useContext, useState } from 'react';

type Props = {
  receiver: string;
};

function ChatScreen({ receiver }: Props) {
  const [message, setMessage] = useState<string>('');
  const { username, messageHistory } = useContext(ChatContext);
  const { sendMessage } = useContext(WebSocketContext);

  return (
    <div className="flex flex-col-reverse w-4/5 bg-stone-800 p-8">
      <input
        className="fixed bottom-5 right-12 border rounded-xl px-4 py-2 w-15/20"
        type="text"
        placeholder="Aa"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            sendMessage(message, receiver);
            setMessage('');
          }
        }}
      />
      <div className="flex flex-col gap-4 overflow-y-scroll p-8 mb-13">
        {messageHistory
          .filter((messageJsonString) => {
            const message = JSON.parse(messageJsonString);
            return (
              (message.type === 'broadcast' && receiver === '') ||
              (message.from === username && message.to === receiver) ||
              (message.from === receiver && message.to === username)
            );
          })
          .map((messageJsonString, i) => {
            const message = JSON.parse(messageJsonString);
            return (
              <Message
                key={i}
                message={message.message}
                mine={username === message.from}
              />
            );
          })}
      </div>
    </div>
  );
}

export default ChatScreen;
