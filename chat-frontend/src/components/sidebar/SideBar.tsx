import UserChat from '@/components/sidebar/UserChar';

function SideBar() {
  const users = ['alice', 'bob', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie', 'charlie'];

  return (
    <div className="w-1/5 bg-gray-800 outline-1 outline-solid outline-gray-900 overflow-y-scroll p-4">
      {users.map((u) => (
        <UserChat key={u} name={u} />
      ))}
    </div>
  );
}

export default SideBar;
