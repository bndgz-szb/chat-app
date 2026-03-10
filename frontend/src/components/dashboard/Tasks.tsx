import TaskFormModal from '@/components/dashboard/TaskFormModal';
import { useDashboardQuery } from '@/state/apiSlice';
import { selectIsAdmin, selectUserId } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import { Link } from 'react-router-dom';

function Tasks() {
	const { data } = useDashboardQuery();
	const user_id = useAppSelector(selectUserId);
	const is_admin = useAppSelector(selectIsAdmin);

	return (
		<div className="flex flex-row p-8 gap-4 flex-wrap">
			{data ? (
				data.map((task) => (
					<div
						key={task.id}
						className="flex flex-col min-h-60 w-55 rounded-xl bg-white text-black p-4 justify-between gap-2"
					>
						<div className="flex flex-col gap-2">
							<div className="text-center font-bold text-lg">{task.name}</div>
							<div className="rounded-md bg-black text-white p-1.5 w-min">
								{task.done ? <>&#10003;Befejezve</> : <>&#9900;Folyamatban</>}
							</div>
							<div className="flex flex-row gap-2 flex-wrap">
								{task.topics.map((topic) => (
									<div
										className="rounded-md bg-black text-white p-1.5"
										key={topic.id}
									>
										{topic.name}
									</div>
								))}
							</div>
						</div>
						<div className="flex flex-col gap-2">
							{task.created_by && (is_admin || task.created_by == user_id) && (
								<div className="flex flex-row justify-between gap-2">
									<div className="p-1.5 text-white rounded-md bg-red-600">
										Törlés
									</div>
									<TaskFormModal
										buttonText="Módosítás"
										buttonStyle="p-1.5 text-white rounded-md bg-black normal-case"
										task={task}
									/>
								</div>
							)}
							{user_id !== -1 && task.chat_id && (
								<Link
									to={'/chat'}
									state={{ chat_id: task.chat_id }}
									className="rounded-md bg-sky-500 text-center text-white border-2 border-black"
								>
									Chat
								</Link>
							)}
						</div>
					</div>
				))
			) : (
				<div>Loading...</div>
			)}
		</div>
	);
}

export default Tasks;
