import TaskFormModal from '@/components/dashboard/TaskFormModal';
import { useCreateTaskMutation } from '@/state/apiSlice';
import type { CreateTaskRequest } from '@/state/requestTypes';
import { Link } from 'react-router-dom';

function ButtonRow() {
	const [sendCreate] = useCreateTaskMutation();

	const handleCreateTask = (
		updated_task: CreateTaskRequest,
		onSuccess: (value: string) => void,
		onError: (reason: any) => void,
		_: number
	) => {
		sendCreate(updated_task).unwrap().then(onSuccess).catch(onError);
	};

	return (
		<div className="flex p-8 flex-row-reverse gap-5">
			<div className="rounded-md p-4 bg-gray-900">Szűrés</div>
			<Link to={'/dashboard/topics'} className="rounded-md p-4 bg-gray-900">
				Tematikák kezelése
			</Link>

			<TaskFormModal
				buttonText="Feladat létrehozása"
				buttonStyle="rounded-md p-4 bg-gray-900 normal-case text-base"
				handleSubmit={handleCreateTask}
			/>
		</div>
	);
}

export default ButtonRow;
