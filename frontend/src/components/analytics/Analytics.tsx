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

type AnalyticsData = {
	tasks: TaskWithAnalytics[];
};

type TaskWithAnalytics = {
	name: string;
	messagesByDays: MessagesByDay[];
	messagesPerUsers: MessagesPerUser[];
};

type MessagesByDay = {
	day: string;
	messages: number;
};

type MessagesPerUser = {
	username: string;
	total_messages: number;
};

function Analytics() {
	// TODO get from api
	const input: AnalyticsData = {
		tasks: [
			{
				name: 'Feladat1',
				messagesByDays: [
					{
						day: '06-13',
						messages: 400,
					},
					{
						day: '06-14',
						messages: 300,
					},
					{
						day: '06-15',
						messages: 300,
					},
					{
						day: '06-16',
						messages: 200,
					},
					{
						day: '06-17',
						messages: 278,
					},
					{
						day: '06-18',
						messages: 189,
					},
				],
				messagesPerUsers: [
					{
						username: 'rajesh',
						total_messages: 90,
					},
					{
						username: 'boti',
						total_messages: 190,
					},
					{
						username: 'jano',
						total_messages: 10,
					},
					{
						username: 'feri',
						total_messages: 40,
					},
					{
						username: 'jon doe',
						total_messages: 95,
					},
				],
			},
			{
				name: 'Feladat2',
				messagesByDays: [
					{
						day: '06-13',
						messages: 400,
					},
					{
						day: '06-14',
						messages: 300,
					},
					{
						day: '06-15',
						messages: 300,
					},
					{
						day: '06-16',
						messages: 200,
					},
					{
						day: '06-17',
						messages: 278,
					},
					{
						day: '06-18',
						messages: 189,
					},
				],
				messagesPerUsers: [
					{
						username: 'rajesh',
						total_messages: 90,
					},
					{
						username: 'boti',
						total_messages: 190,
					},
					{
						username: 'jano',
						total_messages: 10,
					},
					{
						username: 'feri',
						total_messages: 40,
					},
					{
						username: 'jon doe',
						total_messages: 95,
					},
				],
			},
			{
				name: 'Feladat3',
				messagesByDays: [
					{
						day: '06-13',
						messages: 400,
					},
					{
						day: '06-14',
						messages: 300,
					},
					{
						day: '06-15',
						messages: 300,
					},
					{
						day: '06-16',
						messages: 200,
					},
					{
						day: '06-17',
						messages: 278,
					},
					{
						day: '06-18',
						messages: 189,
					},
				],
				messagesPerUsers: [
					{
						username: 'rajesh',
						total_messages: 90,
					},
					{
						username: 'boti',
						total_messages: 190,
					},
					{
						username: 'jano',
						total_messages: 10,
					},
					{
						username: 'feri',
						total_messages: 40,
					},
					{
						username: 'jon doe',
						total_messages: 95,
					},
				],
			},
		],
	};

	const customTooltip = (o: TooltipContentProps) => {
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
					<div>Total messages: {d.total_messages}</div>
				</div>
			);
		}
		return null;
	};

	return (
		<Card className="bg-white w-5xl p-4 my-8">
			<CardContent>
				<div className="flex flex-col gap-8">
					{input.tasks.map((task) => {
						const generateColors = (count: number) =>
							Array.from({ length: count }, (_, i) => {
								const hue = (i * 360) / count;
								return `hsl(${hue}, 70%, 55%)`;
							});
						const COLORS = generateColors(input.tasks[0].messagesByDays.length);
						const MyCustomPie = (props: PieSectorShapeProps) => {
							return (
								<Sector {...props} fill={COLORS[props.index % COLORS.length]} />
							);
						};

						return (
							<div className="flex flex-col">
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
										<Tooltip />
									</LineChart>
									<PieChart className="w-full h-75" responsive>
										<Pie
											data={task.messagesPerUsers}
											dataKey="total_messages"
											nameKey="username"
											cx="50%"
											cy="50%"
											outerRadius={120}
											shape={MyCustomPie}
											label={({ name, percent }) =>
												`${name} ${((percent ?? 1) * 100).toFixed(0)}%`
											}
										/>
										<Tooltip content={customTooltip} />
									</PieChart>
								</div>
							</div>
						);
					})}
				</div>
			</CardContent>
		</Card>
	);
}

export default Analytics;
