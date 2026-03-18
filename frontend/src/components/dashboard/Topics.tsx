import DeleteModal from '@/components/dashboard/DeleteModal';
import { useTopicsQuery } from '@/state/apiSlice';

function Topics() {
	const { data } = useTopicsQuery();

	return data ? (
		<div className="flex flex-col gap-4 p-4 self-start">
			<div className="rounded-md bg-black text-white p-2 w-fit">
				{/* TODO create topic modal */}
				Tematika létrehozása
			</div>
			<div className="text-white text-lg font-bold">Tematikák</div>
			<div className="flex flex-row gap-2 flex-wrap">
				{data.map((topic) => (
					<div
						className="flex gap-1 rounded-md text-white bg-black p-2 items-center"
						key={topic.id}
					>
						{/* TODO delete topic modal */}
						<div className="h-full self-center">{topic.name} </div>
						<DeleteModal
							title={topic.name}
							buttonText="&#10005;"
							buttonStyle="p-0 h-full min-w-1 w-5 text-white rounded-md normal-case"
							confirmText={`Biztosan törli a tematikát?`}
							handleDelete={() => {}}
						/>
					</div>
				))}
			</div>
		</div>
	) : (
		<div>Loading topics...</div>
	);
}

export default Topics;
