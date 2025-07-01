type Props = {
  name: string;
};

function UserChat({ name }: Props) {
  return <div className="hover:rounded-md hover:bg-gray-700 p-8 font-bold">{name}</div>;
}

export default UserChat;
