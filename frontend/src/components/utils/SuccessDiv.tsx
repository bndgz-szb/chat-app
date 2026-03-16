type Props = {
	message?: string;
};

function SuccessDiv({ message }: Props) {
	return (
		<div className="mb-6 text-center text-green-500 font-bold bg-green-200 rounded-lg border border-green-600 p-2">
			{message}
		</div>
	);
}

export default SuccessDiv;
