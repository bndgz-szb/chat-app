type Props = {
  name: string;
  onClick: (receiver: string) => void;
  selected: boolean;
};

function UserChat({ name, onClick, selected }: Props) {
  return (
    <div
      onClick={() => onClick(name)}
      className={`${
        selected
          ? 'rounded-md bg-teal-800'
          : 'hover:rounded-md hover:bg-gray-700'
      } p-8 font-bold`}
    >
      {name === '' ? 'Broadcast' : name}
    </div>
  );
}

export default UserChat;
