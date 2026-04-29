type Props = {
	type: string;
	name: string;
	label: string;
	value: string;
	placeholder: string;
	onChange: (name: string) => void;
};

const InputField = ({
	type,
	name,
	label,
	value,
	onChange,
	placeholder,
}: Props) => {
	return (
		<div>
			<label htmlFor={name} className="block mb-1">
				{label}
			</label>

			<input
				type={type}
				id={name}
				placeholder={placeholder}
				className="w-full px-4 py-2 rounded-md text-black outline-none bg-white placeholder-gray-500"
				value={value}
				onChange={(e) => onChange(e.target.value)}
			/>
		</div>
	);
};

export default InputField;
