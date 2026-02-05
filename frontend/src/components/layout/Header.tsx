function Header() {
	{
		/* TODO Show buttons according to user permissions */
	}

	return (
		<div className="w-full bg-gray-800 h-30 align-middle p-4 flex justify-between">
			<div className="p-8 font-bold">Site Name</div>
			<div className="flex gap-2">
				<div className="p-8 font-bold">Chat</div>
				<div className="p-8 font-bold">Irányítópult</div>
				<div className="p-8 font-bold">Analitika</div>
				<div className="p-8 bg-gray-950 rounded-md font-bold">
					Bejelentkezés
				</div>
			</div>
		</div>
	);
}
export default Header;
