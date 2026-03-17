import ErrorDiv from '@/components/utils/ErrorDiv';
import ParticipantsModal from '@/components/dashboard/ParticipantsModal';
import {
	useAllUsersQuery,
	useLazyTaskParticipantsQuery,
	useTopicsQuery,
} from '@/state/apiSlice';
import { selectUserId } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import type {
	TaskParticipant,
	TaskWithTopic,
	Topic,
} from '@/state/responseTypes';
import { Autocomplete, Button, Modal, Switch, TextField } from '@mui/material';
import { useEffect, useState } from 'react';
import SuccessDiv from '@/components/utils/SuccessDiv';
import type { CreateTaskRequest } from '@/state/requestTypes';

type Props = {
	buttonText: string;
	buttonStyle: string;
	task?: TaskWithTopic;
	handleSubmit: (
		updated_task: CreateTaskRequest,
		onSuccess: (value: string) => void,
		onError: (reason: any) => void,
		taskId: number
	) => void;
};

function TaskFormModal({ buttonText, buttonStyle, task, handleSubmit }: Props) {
	const [error, setError] = useState<string>('');
	const [successMessage, setSuccessMessage] = useState<string>('');
	const [open, setOpen] = useState<boolean>(false);
	const [isDone, setIsDone] = useState<boolean>(task ? task.done : false);
	const [taskName, setTaskName] = useState<string>(task ? task.name : '');
	const [taskTopics, setTaskTopics] = useState<Topic[]>(
		task ? task.topics : []
	);
	const [taskParticipants, setTaskParticipants] = useState<TaskParticipant[]>(
		[]
	);

	const topics = useTopicsQuery();
	const participants = useAllUsersQuery();
	const [getTaskParticipants] = useLazyTaskParticipantsQuery();
	const userId = useAppSelector(selectUserId);

	useEffect(() => {
		if (open && taskParticipants.length === 0 && task) {
			getTaskParticipants({ task_id: task.id })
				.unwrap()
				.then((data) => setTaskParticipants(data));
		}
	}, [open]);

	const resetFormState = () => {
		setIsDone(false);
		setTaskName('');
		setTaskTopics([]);
		setTaskParticipants([]);
	};

	const onClick = () => {
		if (taskName === '') {
			setError('A feladat neve kötelező mező!');
			return;
		}
		if (taskParticipants.length === 0) {
			setError('A feladatnak kell, hogy legyen legalább 1 résztvevője!');
			return;
		}

		handleSubmit(
			{
				name: taskName,
				done: isDone,
				topics: taskTopics,
				participants: taskParticipants,
			},
			(value) => {
				setSuccessMessage(value);
				resetFormState();
			},
			(reason) => setError(reason.data?.detail),
			task?.id ?? -1
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
							<label htmlFor="task-name" className="block mb-1">
								Feladat neve
							</label>
							<input
								type="text"
								name="task-name"
								id="task-name"
								value={taskName}
								onChange={(e) => setTaskName(e.target.value)}
								placeholder="Feladat1"
								className="w-full px-4 py-2 rounded-md outline-none border border-1 placeholder-gray-500"
							/>
						</div>

						<Autocomplete
							multiple
							value={taskTopics}
							isOptionEqualToValue={(option, value) => option.id === value.id}
							onChange={(_: any, newValue: Topic[]) => setTaskTopics(newValue)}
							id="topics"
							loading={topics.isLoading}
							loadingText="Tematikák betöltése folyamatban..."
							noOptionsText="Nincs további tematika"
							options={topics.data ?? []}
							getOptionLabel={(option) => option.name}
							getOptionKey={(option) => option.id}
							filterSelectedOptions
							renderInput={(params) => (
								<TextField
									{...params}
									label="Tematikák"
									placeholder="Feladat tematikái"
								/>
							)}
						/>

						<ParticipantsModal
							allUsers={participants.data?.filter((user) => user.id !== userId)}
							initialGuests={taskParticipants.filter(
								(user) => user.role === 'guest'
							)}
							initialMembers={taskParticipants.filter(
								(user) => user.role === 'member'
							)}
							setTaskParticipants={setTaskParticipants}
						/>

						<div className="flex flex-row flex-wrap gap-2">
							{taskParticipants.map((participant) => (
								<div className="rounded-md border p-1" key={participant.id}>
									{participant.name}:{participant.role}
								</div>
							))}
						</div>

						<div>
							<div className="flex flex-row w-full justify-between">
								Státusz
								<Switch
									color="info"
									checked={isDone}
									onChange={() => setIsDone(!isDone)}
								/>
							</div>
							<div className="text-gray-500">
								{isDone ? 'Befejezve' : 'Folyamatban'}
							</div>
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

export default TaskFormModal;
