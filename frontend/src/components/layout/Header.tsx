import { selectIsAdmin, selectUser } from '@/state/authSlice';
import { useAppSelector } from '@/state/hooks';
import { Link, useLocation } from 'react-router-dom';
import LanguageSelector from '@/components/utils/LanguageSelector';
import { useTranslation } from 'react-i18next';
import { useState } from 'react';
import MenuIcon from '@mui/icons-material/Menu';
import MenuOpenIcon from '@mui/icons-material/MenuOpen';

// ChatGPT generated almost everything
function Header() {
	const [open, setOpen] = useState(false);
	const username = useAppSelector(selectUser);
	const isAdmin = useAppSelector(selectIsAdmin);
	const { t } = useTranslation();
	const location = useLocation();

	return (
		<nav className="w-full bg-gray-800 shadow-md flex items-center">
			<div className="w-full h-1/6 p-4 flex justify-between mx-auto items-center">
				{/* Mobile Button */}
				<button className="lg:hidden" onClick={() => setOpen(!open)}>
					{open ? (
						<MenuOpenIcon fontSize="large" />
					) : (
						<MenuIcon fontSize="large" />
					)}
				</button>
				<div className="lg:hidden font-bold">
					{t(location.pathname.split('/')[1])}
				</div>

				{/* Site Menu */}
				<div className="flex">
					<div className="p-8 font-bold">ChatApp</div>
					<LanguageSelector />
				</div>

				{/* Desktop Menu */}
				<div className="hidden lg:flex gap-2">
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
						<Link
							to={'/login'}
							className="p-8 bg-gray-950 rounded-md font-bold"
						>
							{t('login')}
						</Link>
					) : (
						<Link
							to={'/logout'}
							className="p-8 bg-gray-950 rounded-md font-bold"
						>
							{t('logout')}
						</Link>
					)}
				</div>
			</div>

			{/* Mobile Menu */}
			<div
				className={`lg:hidden fixed top-0 left-0 z-20 w-full h-screen bg-gray-800 transform transition-transform duration-300 ease-in-out ${
					open ? 'translate-x-0' : '-translate-x-full'
				}`}
			>
				<div className="flex justify-between items-center p-4 mx-auto border-b">
					<button onClick={() => setOpen(false)}>
						<MenuOpenIcon fontSize="large" />
					</button>
					<div className="lg:hidden font-bold text-2xl">
						{t(location.pathname.split('/')[1])}
					</div>
					{/* Site Menu */}
					<div className="flex">
						<div className="p-8 font-bold">ChatApp</div>
					</div>
				</div>

				<div className="flex flex-col items-center mt-10 gap-6 text-lg">
					{username !== '' && (
						<Link
							onClick={() => setOpen(false)}
							to={'/chat'}
							className="p-8 font-bold"
						>
							{t('chat')}
						</Link>
					)}
					<Link
						onClick={() => setOpen(false)}
						to={'/dashboard'}
						className="p-8 font-bold"
					>
						{t('dashboard')}
					</Link>
					{isAdmin && (
						<Link
							onClick={() => setOpen(false)}
							to={'/analytics'}
							className="p-8 font-bold"
						>
							{t('analytics')}
						</Link>
					)}
					{username === '' ? (
						<Link
							onClick={() => setOpen(false)}
							to={'/login'}
							className="p-8 bg-gray-950 rounded-md font-bold"
						>
							{t('login')}
						</Link>
					) : (
						<Link
							onClick={() => setOpen(false)}
							to={'/logout'}
							className="p-8 bg-gray-950 rounded-md font-bold"
						>
							{t('logout')}
						</Link>
					)}
				</div>
			</div>
		</nav>
	);
}
export default Header;
