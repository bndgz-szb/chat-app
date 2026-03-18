import { Button, Modal } from '@mui/material';
import { useState } from 'react';

type Props = {
	title: string;
	buttonText: string;
	buttonStyle: string;
	confirmText: string;
	handleDelete: () => void;
};

function DeleteModal({
	title,
	buttonText,
	buttonStyle,
	confirmText,
	handleDelete,
}: Props) {
	const [open, setOpen] = useState<boolean>(false);

	const onClick = () => {
		handleDelete();
		setOpen(false);
	};

	return (
		<div>
			<Button className={buttonStyle} onClick={() => setOpen(true)}>
				{buttonText}
			</Button>
			<Modal open={open} onClose={() => setOpen(false)}>
				<div className="absolute inset-0.5 flex items-center justify-center p-4 flex-col">
					<div className="flex flex-col gap-4 rounded-lg p-10 w-full max-w-md bg-white text-black">
						<h1 className="font-bold">{title}</h1>
						{confirmText}
						<div className="flex gap-1">
							<Button
								variant="outlined"
								disableElevation
								className="w-full p-2 rounded-md text-center"
								onClick={() => setOpen(false)}
							>
								Mégsem
							</Button>
							<Button
								className="w-full bg-red-600 text-white p-2 rounded-md text-center"
								onClick={onClick}
							>
								Törlés
							</Button>
						</div>
					</div>
				</div>
			</Modal>
		</div>
	);
}

export default DeleteModal;
