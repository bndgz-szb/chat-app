import Header from '@/components/layout/Header';

type Props = {
	children: React.ReactNode;
};

function Layout(props: Props) {
	return (
		<div className="flex flex-col h-full">
			<Header />
			{props.children}
		</div>
	);
}

export default Layout;
