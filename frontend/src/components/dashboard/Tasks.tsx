import DeleteModal from '@/components/dashboard/DeleteModal';
import TaskFormModal from '@/components/dashboard/TaskFormModal';
import LoadingDiv from '@/components/utils/LoadingDiv';
import {
	useDashboardQuery,
	useDeleteTaskMutation,
	useUpdateTaskMutation,
} from '@/state/apiSlice';
import { selectIsAdmin, selectUserId } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import type { CreateTaskRequest } from '@/state/requestTypes';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

function Tasks() {
	const { data } = useDashboardQuery();
	const user_id = useAppSelector(selectUserId);
	const is_admin = useAppSelector(selectIsAdmin);
	const [sendUpdate] = useUpdateTaskMutation();
	const [sendDeleteTask] = useDeleteTaskMutation();
	const { t } = useTranslation();

	const handleModifyTask = (
		updated_task: CreateTaskRequest,
		onSuccess: (value: string) => void,
		onError: (reason: any) => void,
		task_id: number
	) => {
		if (task_id === -1) {
			onError({ data: { detail: 'Illegal task id for task modification' } });
			return;
		}
		sendUpdate({
			task_id,
			updated_task,
		})
			.unwrap()
			.then(onSuccess)
			.catch(onError);
	};

	const handleDelete =
		(task_id: number) =>
		(onSuccess: (value: string) => void, onError: (reason: any) => void) => {
			sendDeleteTask({
				task_id,
			})
				.unwrap()
				.then(onSuccess)
				.catch(onError);
		};

	return (
		<div className="flex flex-col lg:flex-row p-8 gap-4 flex-wrap w-screen">
			{data ? (
				data.map((task) => (
					<div
						key={task.id}
						className="flex flex-col min-h-60 w-9/10 max-w-md lg:w-55 rounded-xl bg-white text-black p-4 justify-between self-center lg:self-auto gap-2"
					>
						<div className="flex flex-col gap-2">
							<div className="text-center font-bold text-lg">{task.name}</div>
							<div className="rounded-md bg-black text-white p-1.5 w-min">
								{task.done ? (
									<>&#10003;{t('done')}</>
								) : (
									<>&#9900;{t('ongoing')}</>
								)}
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
									<DeleteModal
										title={task.name}
										buttonText={t('delete')}
										buttonStyle="p-1.5 text-white rounded-md bg-red-600 normal-case"
										confirmText={t('confirm_task_delete')}
										handleDelete={handleDelete(task.id)}
									/>

									<TaskFormModal
										buttonText={t('modify')}
										buttonStyle="p-1.5 text-white rounded-md bg-black normal-case"
										task={task}
										handleSubmit={handleModifyTask}
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
				<LoadingDiv />
			)}
		</div>
	);
}

export default Tasks;
