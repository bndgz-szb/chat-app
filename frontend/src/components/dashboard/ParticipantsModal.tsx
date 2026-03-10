import type { TaskParticipant } from '@/state/requestTypes';
import type { Participant } from '@/state/responseTypes';
import { Autocomplete, Button, Modal, TextField } from '@mui/material';
import { useState } from 'react';

type ParticipantsModalProps = {
	allUsers?: Participant[];
	initialGuests: TaskParticipant[];
	initialUsers: TaskParticipant[];
	setTaskParticipants: (newTaskParticipants: TaskParticipant[]) => void;
};

function ParticipantsModal({
	allUsers,
	initialGuests,
	initialUsers,
	setTaskParticipants,
}: ParticipantsModalProps) {
	const [open, setOpen] = useState<boolean>(false);
	const [guests, setGuests] = useState<Participant[]>(initialGuests);
	const [users, setUsers] = useState<Participant[]>(initialUsers);

	const handleSubmit = () => {
		const taskParticipants: TaskParticipant[] = guests
			.map(
				(guest) =>
					({
						...guest,
						role: 'guest',
					}) as TaskParticipant
			)
			.concat(
				users.map((user) => ({ ...user, role: 'user' }) as TaskParticipant)
			);

		setTaskParticipants(taskParticipants);
		setOpen(false);
	};

	return (
		<div className="w-full bg-slate-900 rounded-md text-center">
			<Button
				variant="text"
				disableElevation
				className="normal-case text-base text-white w-full p-2"
				onClick={() => setOpen(true)}
			>
				Résztvevők módosítása
			</Button>
			<Modal open={open} onClose={() => setOpen(false)}>
				<div className="absolute inset-0.5 grow flex items-center justify-center p-4 flex-col">
					<div className="flex flex-col gap-4 rounded-lg p-10 w-full max-w-lg bg-white text-black">
						<div>
							<label htmlFor="task-participants" className="block mb-1">
								Vendég felhasználók
							</label>
							<Autocomplete
								multiple
								value={guests}
								onChange={(_: any, newValue: Participant[]) =>
									setGuests(newValue)
								}
								id="task-participants"
								loading={allUsers === undefined}
								loadingText="Résztvevők betöltése folyamatban..."
								noOptionsText="Nincs további felhasználó"
								options={
									allUsers
										? allUsers.filter((user) =>
												users.every((other) => user.id !== other.id)
											)
										: []
								}
								getOptionLabel={(option) => `${option.name}`}
								filterSelectedOptions
								renderInput={(params) => (
									<TextField
										{...params}
										label="Feladat résztvevői"
										placeholder="Feladat résztvevői"
									/>
								)}
							/>
						</div>
						<div>
							<label htmlFor="task-participants" className="block mb-1">
								Teljes körű felhasználók
							</label>
							<Autocomplete
								multiple
								value={users}
								onChange={(_: any, newValue: Participant[]) =>
									setUsers(newValue)
								}
								id="task-participants"
								loading={allUsers === undefined}
								loadingText="Résztvevők betöltése folyamatban..."
								noOptionsText="Nincs további felhasználó"
								options={
									allUsers
										? allUsers.filter((user) =>
												guests.every((other) => user.id !== other.id)
											)
										: []
								}
								getOptionLabel={(option) => `${option.name}`}
								filterSelectedOptions
								renderInput={(params) => (
									<TextField
										{...params}
										label="Feladat résztvevői"
										placeholder="Feladat résztvevői"
									/>
								)}
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
								onClick={handleSubmit}
								className="w-full bg-slate-900 text-white p-2 rounded-md text-center"
							>
								Hozzáadás
							</Button>
						</div>
					</div>
				</div>
			</Modal>
		</div>
	);
}

export default ParticipantsModal;
