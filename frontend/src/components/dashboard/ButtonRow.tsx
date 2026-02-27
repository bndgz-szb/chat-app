import { Link } from 'react-router-dom';

function ButtonRow() {
	return (
		<div className="flex p-8 flex-row-reverse gap-5">
			<div className="rounded-md p-4 bg-gray-900">Szűrés</div>
			<Link to={'/dashboard/topics'} className="rounded-md p-4 bg-gray-900">
				Tematikák kezelése
			</Link>
			<Link
				to={'/dashboard/create_task'}
				className="rounded-md p-4 bg-gray-900"
			>
				Feladat létrehozása
			</Link>
		</div>
	);
}

export default ButtonRow;
