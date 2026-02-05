type Props = {
	error: string;
};

function ErrorDiv({ error }: Props) {
	return (
		<div className="mb-6 text-center text-red-500 font-bold bg-red-200 rounded-lg border border-red-600 p-2">
			{error}
		</div>
	);
}

export default ErrorDiv;
