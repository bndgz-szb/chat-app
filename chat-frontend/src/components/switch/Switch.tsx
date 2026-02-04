import { useState } from 'react';
import '@/components/switch/Switch.css';

function Switch() {
	const [isOn, setIsOn] = useState(false);

	function handleToggle() {
		setIsOn(!isOn);
	}

	return (
		<label className="switch">
			<input type="checkbox" checked={isOn} onChange={handleToggle} />
			<span className="slider round"></span>
		</label>
	);
}

export default Switch;
