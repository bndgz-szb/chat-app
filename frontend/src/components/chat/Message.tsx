type Props = {
  message: string;
  mine: boolean;
};

function Message({ message, mine }: Props) {
  return mine ? (
    <div className="ml-auto w-max bg-blue-400 rounded-lg justify-self-end py-2 px-3">
      {message}
    </div>
  ) : (
    <div className="mr-auto w-max bg-stone-400 rounded-lg justify-self-end py-2 px-3">
      {message}
    </div>
  );
}

export default Message;
