import { selectIsAdmin, selectUser } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import { Link } from 'react-router-dom';
import LanguageSelector from '@/components/utils/LanguageSelector';
import { useTranslation } from 'react-i18next';

function Header() {
	const username = useAppSelector(selectUser);
	const isAdmin = useAppSelector(selectIsAdmin);
	const { t } = useTranslation();

	return (
		<div className="w-full bg-gray-800 h-1/6 items-center p-4 flex justify-between">
			<div className="flex">
				<div className="p-8 font-bold">ChatApp</div>
				<LanguageSelector />
			</div>
			<div className="flex gap-2">
				{username !== '' && (
					<Link to={'/chat'} className="p-8 font-bold">
						{t('chat')}
					</Link>
				)}
				<Link to={'/dashboard'} className="p-8 font-bold">
					{t('dashboard')}
				</Link>
				{isAdmin && (
					<Link to={'/analytics'} className="p-8 font-bold">
						{t('analytics')}
					</Link>
				)}
				{username === '' ? (
					<Link to={'/login'} className="p-8 bg-gray-950 rounded-md font-bold">
						{t('login')}
					</Link>
				) : (
					<Link to={'/logout'} className="p-8 bg-gray-950 rounded-md font-bold">
						{t('logout')}
					</Link>
				)}
			</div>
		</div>
	);
}
export default Header;
