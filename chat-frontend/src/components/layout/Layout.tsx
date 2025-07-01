import ChatScreen from '@/components/chat-screen/ChatScreen';
import SideBar from '@/components/sidebar/SideBar';

function Layout() {
  return (
    <div className="flex h-full w-full justify-between gap-1">
      <SideBar />
      <ChatScreen />
    </div>
  );
}

export default Layout;
