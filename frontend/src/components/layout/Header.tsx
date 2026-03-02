import { selectUser } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import { Link } from 'react-router-dom';

function Header() {
	{
		/* TODO Show buttons according to user permissions */
	}
	const username = useAppSelector(selectUser);

	return (
		<div className="w-full bg-gray-800 h-1/6 max-h-30 align-middle p-4 flex justify-between">
			<div className="p-8 font-bold">Site Name</div>
			<div className="flex gap-2">
				<Link to={'/chat'} className="p-8 font-bold">
					Chat
				</Link>
				<Link to={'/dashboard'} className="p-8 font-bold">
					Irányítópult
				</Link>
				<Link to={'/analytics'} className="p-8 font-bold">
					Analitika
				</Link>
				{username === '' ? (
					<Link to={'/login'} className="p-8 bg-gray-950 rounded-md font-bold">
						Bejelentkezés
					</Link>
				) : (
					<Link to={'/logout'} className="p-8 bg-gray-950 rounded-md font-bold">
						Kijelentkezés
					</Link>
				)}
			</div>
		</div>
	);
}
export default Header;
