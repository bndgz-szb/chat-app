import { useDeleteTaskMutation } from '@/state/apiSlice';
import { Button, Modal } from '@mui/material';
import { useState } from 'react';

type Props = {
	task_id: number;
};

function DeleteTaskModal({ task_id }: Props) {
	const [open, setOpen] = useState<boolean>(false);
	const [sendDeleteTask] = useDeleteTaskMutation();

	const handleDelete = () => {
		sendDeleteTask({ task_id });
		setOpen(false);
	};

	return (
		<div>
			<Button
				className="p-1.5 text-white rounded-md bg-red-600 normal-case"
				onClick={() => setOpen(true)}
			>
				Törlés
			</Button>
			<Modal open={open} onClose={() => setOpen(false)}>
				<div className="absolute inset-0.5 flex items-center justify-center p-4 flex-col">
					<div className="flex flex-col gap-4 rounded-lg p-10 w-full max-w-md bg-white text-black">
						Biztosan törli a feladatot?
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
								onClick={handleDelete}
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

export default DeleteTaskModal;
