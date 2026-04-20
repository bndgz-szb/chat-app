import { useAnalyticsQuery } from '@/state/apiSlice';
import { Card, CardContent } from '@mui/material';
import {
	Line,
	LineChart,
	Pie,
	PieChart,
	Sector,
	Tooltip,
	XAxis,
	YAxis,
	type PieSectorShapeProps,
	type TooltipContentProps,
} from 'recharts';
import { useTranslation } from 'react-i18next';
import LoadingDiv from '@/components/utils/LoadingDiv';

// ChatGPT generated parts within this component
function Analytics() {
	const { data } = useAnalyticsQuery();
	const { t } = useTranslation();

	const customPieTooltip = (o: TooltipContentProps) => {
		const { active, payload } = o;
		if (active && payload && payload.length) {
			const d = payload[0].payload;
			return (
				<div
					style={{
						background: 'white',
						border: '1px solid #ccc',
						padding: '8px',
					}}
				>
					<div>
						<strong>{d.username}</strong>
					</div>
					<div>
						{t('total_messages')}: {d.total_messages}
					</div>
				</div>
			);
		}
		return null;
	};
	const customLineTooltip = (o: TooltipContentProps) => {
		const { active, payload } = o;
		if (active && payload && payload.length) {
			const d = payload[0].payload;
			return (
				<div
					style={{
						background: 'white',
						border: '1px solid #ccc',
						padding: '8px',
					}}
				>
					<div>
						<strong>{d.day}</strong>
					</div>
					<div>
						{t('messages')}: {d.messages}
					</div>
				</div>
			);
		}
		return null;
	};

	return (
		<Card className="bg-white w-5xl p-4 my-8 overflow-y-scroll">
			<CardContent>
				<div className="flex flex-col gap-8">
					{data ? (
						data.map((task) => {
							const generateColors = (count: number) =>
								Array.from({ length: count }, (_, i) => {
									const hue = (i * 360) / count;
									return `hsl(${hue}, 70%, 55%)`;
								});
							const COLORS = generateColors(task.messagesPerUsers.length);
							const MyCustomPie = (props: PieSectorShapeProps) => {
								return (
									<Sector
										{...props}
										fill={COLORS[props.index % COLORS.length]}
									/>
								);
							};

							return (
								<div className="flex flex-col" key={task.name}>
									<h2 className="m-4 text-xl font-bold">{task.name}</h2>
									<div className="flex justify-between">
										<LineChart
											className="w-full h-75"
											data={task.messagesByDays}
											responsive
										>
											<XAxis dataKey="day" />
											<YAxis />
											<Line type="monotone" dataKey="messages" />
											<Tooltip content={customLineTooltip} />
										</LineChart>
										<PieChart className="w-full h-75" responsive>
											<Pie
												data={task.messagesPerUsers}
												dataKey="total_messages"
												nameKey="username"
												cx="50%"
												cy="50%"
												outerRadius={105}
												shape={MyCustomPie}
												label={({ name, percent }) =>
													`${name} ${((percent ?? 1) * 100).toFixed(0)}%`
												}
											/>
											<Tooltip content={customPieTooltip} />
										</PieChart>
									</div>
								</div>
							);
						})
					) : (
						<LoadingDiv />
					)}
				</div>
			</CardContent>
		</Card>
	);
}

export default Analytics;
