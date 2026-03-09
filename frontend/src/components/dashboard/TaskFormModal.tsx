import ParticipantsModal from '@/components/dashboard/ParticipantsModal';
import { useTopicsQuery } from '@/state/apiSlice';
import type { TaskParticipant } from '@/state/requestTypes';
import type { Topic } from '@/state/responseTypes';
import { Autocomplete, Button, Modal, Switch, TextField } from '@mui/material';
import { useState } from 'react';

function TaskFormModal() {
	const [open, setOpen] = useState(false);
	const [isDone, setIsDone] = useState<boolean>(false);
	const [taskName, setTaskName] = useState<string>('');
	const [taskTopics, setTaskTopics] = useState<Topic[]>([]);
	const [taskParticipants, setTaskParticipants] = useState<TaskParticipant[]>(
		[]
	);
	const topics = useTopicsQuery();

	const participants = [
		{ id: 1, name: 'Résztvevő1' },
		{ id: 2, name: 'Résztvevő2' },
	];

	return (
		<div>
			<Button
				variant="contained"
				disableElevation
				className="rounded-md p-4 bg-gray-900 normal-case text-base"
				onClick={() => setOpen(true)}
			>
				Feladat létrehozása
			</Button>
			<Modal open={open} onClose={() => setOpen(false)}>
				<div className="absolute inset-0.5 grow flex items-center justify-center p-4 flex-col">
					<div className="flex flex-col gap-4 rounded-lg p-10 w-full max-w-md bg-white text-black">
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
							allUsers={participants}
							initialGuests={taskParticipants.filter(
								(user) => user.role === 'guest'
							)}
							initialUsers={taskParticipants.filter(
								(user) => user.role === 'user'
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

						{/* TODO create task */}
						<div className="flex gap-1">
							<Button
								variant="outlined"
								disableElevation
								className="w-full p-2 rounded-md text-center"
								onClick={() => setOpen(false)}
							>
								Mégsem
							</Button>
							<div className="w-full bg-slate-900 text-white p-2 rounded-md text-center">
								Feladat létrehozása
							</div>
						</div>
					</div>
				</div>
			</Modal>
		</div>
	);
}

export default TaskFormModal;
