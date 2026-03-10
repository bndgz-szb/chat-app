import Header from '@/components/layout/Header';

type Props = {
	children: React.ReactNode;
};

function Layout(props: Props) {
	return (
		<div className="h-screen w-screen flex flex-col font-[system-ui,_Avenir,_Helvetica,_Arial,_sans-serif] leading-normal font-normal [color-scheme:light_dark] text-white/87 bg-neutral-800 antialiased m-0 place-items-center min-h-screen">
			<Header />
			{props.children}
		</div>
	);
}

export default Layout;
