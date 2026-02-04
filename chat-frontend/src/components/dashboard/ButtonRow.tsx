import { Link } from 'react-router-dom';

function ButtonRow() {
	return (
		<div className="flex p-8 flex-row-reverse gap-5">
			<div className="rounded-md p-4 bg-gray-900">Szűrés</div>
			<Link
				style={{ color: 'white' }}
				to={'/dashboard/topics'}
				className="rounded-md p-4 bg-gray-900"
			>
				Tematikák kezelése
			</Link>
			<div className="rounded-md p-4 bg-gray-900">Feladat létrehozása</div>
		</div>
	);
}

export default ButtonRow;
