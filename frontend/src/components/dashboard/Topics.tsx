import { useTopicsQuery } from '@/state/apiSlice';

function Topics() {
	const { data } = useTopicsQuery();

	return data ? (
		<div className="flex flex-col gap-4 p-4">
			<div className="rounded-md bg-black text-white p-2 w-fit">
				{/* TODO create topic modal */}
				Tematika létrehozása
			</div>
			<div className="text-white text-lg font-bold">Tematikák</div>
			<div className="flex flex-row gap-2 flex-wrap">
				{data.map((topic) => (
					<div className="rounded-md text-white bg-black p-2" key={topic.id}>
						{/* TODO delete topic modal */}
						{topic.name} &#10005;
					</div>
				))}
			</div>
		</div>
	) : (
		<div>Loading topics...</div>
	);
}

export default Topics;
