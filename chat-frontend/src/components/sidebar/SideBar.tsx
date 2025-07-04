import UserChat from '@/components/sidebar/UserChat';
import { ChatContext } from '@/contexts/ChatContext';
import { useContext } from 'react';

type Props = {
  selectChat: (receiver: string) => void;
  selectedChat: string;
};

function SideBar({ selectChat, selectedChat }: Props) {
  const { onlineUsers } = useContext(ChatContext);

  return (
    <div className="w-1/5 bg-gray-800 outline-1 outline-solid outline-gray-900 overflow-y-scroll p-4">
      <UserChat
        key=""
        name=""
        onClick={selectChat}
        selected={'' === selectedChat}
      />
      {onlineUsers.map((u) => (
        <UserChat
          key={u}
          name={u}
          onClick={selectChat}
          selected={u === selectedChat}
        />
      ))}
    </div>
  );
}

export default SideBar;
