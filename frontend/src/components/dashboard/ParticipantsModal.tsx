import { selectUser, selectUserId } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import {
	ChatRole,
	type Participant,
	type TaskParticipant,
} from '@/state/responseTypes';
import { Autocomplete, Button, Modal, TextField } from '@mui/material';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

type ParticipantsModalProps = {
	allUsers?: Participant[];
	initialGuests: TaskParticipant[];
	initialMembers: TaskParticipant[];
	owner?: TaskParticipant;
	setTaskParticipants: (newTaskParticipants: TaskParticipant[]) => void;
};

function ParticipantsModal({
	allUsers,
	initialGuests,
	initialMembers,
	owner,
	setTaskParticipants,
}: ParticipantsModalProps) {
	const userId = useAppSelector(selectUserId);
	const username = useAppSelector(selectUser);
	const [open, setOpen] = useState<boolean>(false);
	const [guests, setGuests] = useState<Participant[]>(initialGuests);
	const [members, setMembers] = useState<Participant[]>(initialMembers);
	const [fixedParticipant, setFixedParticipant] = useState<TaskParticipant>(
		owner ?? {
			id: userId,
			name: username,
			role: ChatRole.owner,
		}
	);
	const { t } = useTranslation();

	useEffect(() => {
		if (members.length === 0) {
			setMembers(initialMembers);
		}
		if (guests.length === 0) {
			setGuests(initialGuests);
		}
		if (owner) {
			setFixedParticipant(owner);
		}
	}, [initialGuests, initialMembers, owner]);

	const handleSubmit = () => {
		const taskParticipants: TaskParticipant[] = guests
			.map(
				(guest) =>
					({
						...guest,
						role: ChatRole.guest,
					}) as TaskParticipant
			)
			.concat(
				members.map(
					(user) => ({ ...user, role: ChatRole.member }) as TaskParticipant
				)
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
				{t('modify_participants')}
			</Button>
			<Modal open={open} onClose={() => setOpen(false)}>
				<div className="absolute inset-0.5 grow flex items-center justify-center p-4 flex-col">
					<div className="flex flex-col gap-4 rounded-lg p-10 w-full max-w-lg bg-white text-black">
						<div>
							<label htmlFor="task-guests" className="block mb-1">
								{t('guests')}
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
								loadingText={t('loading')}
								noOptionsText={t('no_options')}
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
										label={t('guests')}
										placeholder={t('guests')}
									/>
								)}
							/>
						</div>

						<div>
							<label htmlFor="task-members" className="block mb-1">
								{t('members')}
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
								loadingText={t('loading')}
								noOptionsText={t('no_options')}
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
										label={t('members')}
										placeholder={t('members')}
									/>
								)}
							/>
						</div>

						<div>
							<label htmlFor="task-admin" className="block mb-1">
								{t('admin')}
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
										label={t('admin')}
										placeholder={t('admin')}
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
								{t('cancel')}
							</Button>
							<Button
								onClick={handleSubmit}
								className="w-full bg-slate-900 text-white p-2 rounded-md text-center"
							>
								{t('modify')}
							</Button>
						</div>
					</div>
				</div>
			</Modal>
		</div>
	);
}

export default ParticipantsModal;
