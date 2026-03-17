import { selectUser, selectUserId } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import type { Participant, TaskParticipant } from '@/state/responseTypes';
import { Autocomplete, Button, Modal, TextField } from '@mui/material';
import { useEffect, useState } from 'react';

type ParticipantsModalProps = {
	allUsers?: Participant[];
	initialGuests: TaskParticipant[];
	initialMembers: TaskParticipant[];
	setTaskParticipants: (newTaskParticipants: TaskParticipant[]) => void;
};

function ParticipantsModal({
	allUsers,
	initialGuests,
	initialMembers,
	setTaskParticipants,
}: ParticipantsModalProps) {
	const [open, setOpen] = useState<boolean>(false);
	const [guests, setGuests] = useState<Participant[]>(initialGuests);
	const [members, setMembers] = useState<Participant[]>(initialMembers);
	const userId = useAppSelector(selectUserId);
	const username = useAppSelector(selectUser);
	const fixedParticipant: TaskParticipant = {
		id: userId,
		name: username,
		role: 'admin',
	};

	useEffect(() => {
		if (members.length === 0) {
			setMembers(initialMembers);
		}
		if (guests.length === 0) {
			setGuests(initialGuests);
		}
	}, [initialGuests, initialMembers]);

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
				members.map((user) => ({ ...user, role: 'member' }) as TaskParticipant)
			);
		taskParticipants.push(fixedParticipant);

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
							<label htmlFor="task-guests" className="block mb-1">
								Vendég felhasználók
							</label>
							<Autocomplete
								multiple
								value={guests}
								isOptionEqualToValue={(option, value) => option.id === value.id}
								onChange={(_: any, newValue: Participant[]) =>
									setGuests(newValue)
								}
								id="task-guests"
								loading={allUsers === undefined}
								loadingText="Résztvevők betöltése folyamatban..."
								noOptionsText="Nincs további felhasználó"
								options={
									allUsers
										? allUsers.filter((user) =>
												members.every((other) => user.id !== other.id)
											)
										: []
								}
								getOptionLabel={(option) => `${option.name}`}
								filterSelectedOptions
								renderInput={(params) => (
									<TextField
										{...params}
										label="Vendég résztvevők"
										placeholder="Vendég résztvevők"
									/>
								)}
							/>
						</div>

						<div>
							<label htmlFor="task-members" className="block mb-1">
								Teljes körű felhasználók
							</label>
							<Autocomplete
								multiple
								value={members}
								isOptionEqualToValue={(option, value) => option.id === value.id}
								onChange={(_: any, newValue: Participant[]) =>
									setMembers(newValue)
								}
								id="task-members"
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

						<div>
							<label htmlFor="task-admin" className="block mb-1">
								Admin felhasználó
							</label>
							<Autocomplete
								multiple
								id="task-admin"
								options={[fixedParticipant.name]}
								defaultValue={[fixedParticipant.name]}
								readOnly
								renderInput={(params) => (
									<TextField
										{...params}
										label="Admin résztvevő"
										placeholder="Admin"
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
								Módosítás
							</Button>
						</div>
					</div>
				</div>
			</Modal>
		</div>
	);
}

export default ParticipantsModal;
