import Message from '@/components/chat-screen/Message';
import { ChatContext } from '@/contexts/ChatContext';
import { useContext } from 'react';

function ChatScreen() {
  const { username, messageHistory } = useContext(ChatContext);

  return (
    <div className="flex flex-col-reverse w-4/5 bg-stone-800 p-8">
      <input
        className="fixed bottom-5 right-12 border rounded-xl px-4 py-2 w-15/20"
        type="text"
        placeholder="Aa"
      />
      <div className="flex flex-col-reverse gap-4 overflow-y-scroll p-8 mb-13">
        {messageHistory.map((messageJsonString, i) => {
          const message = JSON.parse(messageJsonString);
          return <Message key={i} message={message.message} mine={username === message.from} />;
        })}
        <Message message="boti" mine={true} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
        <Message message="boti" mine={true} />
        <Message message="boti" mine={true} />
        <Message message="boti" mine={true} />
        <Message message="boti" mine={true} />
        <Message message="boti" mine={true} />
        <Message message="jano" mine={false} />
        <Message message="jano" mine={false} />
      </div>
    </div>
  );
}

export default ChatScreen;
