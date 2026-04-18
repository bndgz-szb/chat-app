import CreateTopicModal from '@/components/dashboard/CreateTopicModal';
import DeleteModal from '@/components/dashboard/DeleteModal';
import LoadingDiv from '@/components/utils/LoadingDiv';
import {
	useCreateTopicMutation,
	useDeleteTopicMutation,
	useTopicsQuery,
} from '@/state/apiSlice';
import type { CreateTopicRequest } from '@/state/requestTypes';
import { useTranslation } from 'react-i18next';

function Topics() {
	const { data } = useTopicsQuery();
	const [sendCreate] = useCreateTopicMutation();
	const [sendDeleteTopic] = useDeleteTopicMutation();
	const { t } = useTranslation();

	const handleCreateTopic = (
		topic: CreateTopicRequest,
		onSuccess: (value: string) => void,
		onError: (reason: any) => void
	) => {
		sendCreate(topic).unwrap().then(onSuccess).catch(onError);
	};

	const handleDelete =
		(topic_id: number) =>
		(onSuccess: (value: string) => void, onError: (reason: any) => void) => {
			sendDeleteTopic({
				topic_id,
			})
				.unwrap()
				.then(onSuccess)
				.catch(onError);
		};

	return data ? (
		<div className="flex flex-col gap-4 p-4 self-start">
			<CreateTopicModal
				buttonText={t('create_topic')}
				buttonStyle={'rounded-md bg-black text-white p-2 w-fit normal-case'}
				handleSubmit={handleCreateTopic}
			/>

			<div className="text-white text-lg font-bold">{t('topics')}</div>
			<div className="flex flex-row gap-2 flex-wrap">
				{data.map((topic) => (
					<div
						className="flex gap-1 rounded-md text-white bg-black p-2 items-center"
						key={topic.id}
					>
						<div className="h-full self-center">{topic.name} </div>
						<DeleteModal
							title={topic.name}
							buttonText="&#10005;"
							buttonStyle="p-0 h-full min-w-1 w-5 text-white rounded-md normal-case"
							confirmText={t('confirm_topic_delete')}
							handleDelete={handleDelete(topic.id)}
						/>
					</div>
				))}
			</div>
		</div>
	) : (
		<LoadingDiv />
	);
}

export default Topics;
