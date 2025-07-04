import ChatScreen from '@/components/chat-screen/ChatScreen';
import SideBar from '@/components/sidebar/SideBar';
import { useState } from 'react';

function Layout() {
  const [receiver, setReceiver] = useState<string>('');

  return (
    <div className="flex h-full w-full justify-between gap-1">
      <SideBar selectChat={setReceiver} selectedChat={receiver} />
      <ChatScreen receiver={receiver} />
    </div>
  );
}

export default Layout;
