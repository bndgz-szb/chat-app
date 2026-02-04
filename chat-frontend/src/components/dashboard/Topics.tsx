function Topics() {
	// TODO query from api
	const topics = [
		{ id: 1, name: 'Tematika1' },
		{ id: 2, name: 'Tematika2' },
		{ id: 3, name: 'Tematika3' },
	];
	return (
		<div className="flex flex-col gap-4 p-4">
			<div className="rounded-md bg-black text-white p-2 w-fit">
				{/* TODO create topic modal */}
				Tematika létrehozása
			</div>
			<div className="text-white text-lg font-bold">Tematikák</div>
			<div className='flex flex-row gap-2 flex-wrap'>
				{topics.map((topic) => (
					<div className="rounded-md text-white bg-black p-2" key={topic.id}>
						{/* TODO delete topic modal */}
						{topic.name} &#10005;
					</div>
				))}
			</div>
		</div>
	);
}

export default Topics;
