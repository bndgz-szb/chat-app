import ButtonRow from '@/components/dashboard/ButtonRow';
import Tasks from '@/components/dashboard/Tasks';

function Dashboard() {
	return (
		<div className='bg-gray-700 grow'>
			<ButtonRow />
			<Tasks />
		</div>
	);
}

export default Dashboard;
