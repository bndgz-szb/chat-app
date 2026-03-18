import ErrorDiv from '@/components/utils/ErrorDiv';

import { Button, Modal } from '@mui/material';
import { useState } from 'react';
import SuccessDiv from '@/components/utils/SuccessDiv';
import type { CreateTopicRequest } from '@/state/requestTypes';

type Props = {
	buttonText: string;
	buttonStyle: string;
	handleSubmit: (
		topic: CreateTopicRequest,
		onSuccess: (value: string) => void,
		onError: (reason: any) => void
	) => void;
};

function CreateTopicModal({ buttonText, buttonStyle, handleSubmit }: Props) {
	const [error, setError] = useState<string>('');
	const [successMessage, setSuccessMessage] = useState<string>('');
	const [open, setOpen] = useState<boolean>(false);
	const [topicName, setTopicName] = useState<string>('');

	const resetFormState = () => {
		setTopicName('');
	};

	const onClick = () => {
		if (topicName === '') {
			setError('A tematika neve kötelező mező!');
			return;
		}

		handleSubmit(
			{
				name: topicName,
			},
			(value) => {
				setSuccessMessage(value);
				resetFormState();
			},
			(reason) => setError(reason.data?.detail)
		);
	};

	return (
		<div>
			<Button
				variant="contained"
				disableElevation
				className={buttonStyle}
				onClick={() => setOpen(true)}
			>
				{buttonText}
			</Button>
			<Modal open={open} onClose={() => setOpen(false)}>
				<div className="absolute inset-0.5 grow flex items-center justify-center p-4 flex-col">
					<div className="flex flex-col gap-4 rounded-lg p-10 w-full max-w-md bg-white text-black">
						{successMessage && <SuccessDiv message={successMessage} />}
						{error && <ErrorDiv error={error} />}

						<div>
							<label htmlFor="topic-name" className="block mb-1">
								Tematika neve
							</label>
							<input
								type="text"
								name="topic-name"
								id="topic-name"
								value={topicName}
								onChange={(e) => setTopicName(e.target.value)}
								placeholder="Tematika1"
								className="w-full px-4 py-2 rounded-md outline-none border border-1 placeholder-gray-500"
							/>
						</div>

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
								className="w-full bg-slate-900 text-white p-2 rounded-md text-cente normal-case"
								onClick={onClick}
							>
								{buttonText}
							</Button>
						</div>
					</div>
				</div>
			</Modal>
		</div>
	);
}

export default CreateTopicModal;
