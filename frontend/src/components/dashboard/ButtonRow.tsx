import TaskFormModal from '@/components/dashboard/TaskFormModal';
import { useCreateTaskMutation } from '@/state/apiSlice';
import type { CreateTaskRequest } from '@/state/requestTypes';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';

function ButtonRow() {
	const [sendCreate] = useCreateTaskMutation();
	const { t } = useTranslation();

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
			<Link to={'/dashboard/topics'} className="rounded-md p-4 bg-gray-900">
				{t('topics')}
			</Link>

			<TaskFormModal
				buttonText={t('create_task')}
				buttonStyle="rounded-md p-4 bg-gray-900 normal-case text-base"
				handleSubmit={handleCreateTask}
			/>
		</div>
	);
}

export default ButtonRow;
