import Switch from '@/components/switch/Switch';

function TaskForm() {
	const topics = [
		{ id: 1, name: 'Tematika1' },
		{ id: 2, name: 'Tematika2' },
		{ id: 3, name: 'Tematika3' },
	];
	const participants = [
		{ id: 1, name: 'Résztvevő1' },
		{ id: 2, name: 'Résztvevő2' },
	];

	return (
		<div className="grow flex items-center justify-center p-4 flex-col">
			<div className="flex flex-col gap-4 rounded-lg p-10 w-full max-w-md bg-white text-black">
				<div>
					<label htmlFor="task-name" className="block mb-1">
						Feladat neve
					</label>
					<input
						type="text"
						name="task-name"
						id="task-name"
						placeholder="Feladat1"
						className="w-full px-4 py-2 rounded-md outline-none border border-1 placeholder-gray-500"
					/>
				</div>

				{/* TODO multiple choice + search */}
				<div>
					<label htmlFor="topics" className="block mb-1">
						Tematikák
					</label>
					<select
						name="topics"
						id="topics"
						className="w-full px-4 py-2 rounded-md outline-none border border-1"
					>
						<option value="-1">Feladat tematikái</option>
						{topics.map((topic) => (
							<option key={topic.id} value={topic.id}>
								{topic.name}
							</option>
						))}
					</select>
				</div>

				{/* TODO modal for participants */}
				<div className="w-full bg-slate-900 text-white p-2 rounded-md text-center">
					Résztvevők hozzáadása
				</div>

				<div className="flex flex-row flex-wrap gap-2">
					{participants.map((participant) => (
						<div className="rounded-md border p-1" key={participant.id}>
							{participant.name} &#10005;
						</div>
					))}
				</div>

				<div>
					<div className="flex flex-row w-full justify-between">
						Státusz
						<Switch />
					</div>
					<div className='text-gray-500'>Folyamatban/Befejezve</div> {/* TODO styling based on switch status */}
				</div>

				{/* TODO create task */}
				<div className="w-full bg-slate-900 text-white p-2 rounded-md text-center">
					Feladat létrehozása
				</div>
			</div>
		</div>
	);
}

export default TaskForm;
