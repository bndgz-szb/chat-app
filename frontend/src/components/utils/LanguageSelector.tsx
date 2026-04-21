import { useEffect, useState } from 'react';
import i18next from 'i18next';
import { useTranslation } from 'react-i18next';
import Select, { type SelectChangeEvent } from '@mui/material/Select';
import { FormControl, InputLabel, MenuItem } from '@mui/material';

type languageOption = { language: string; code: string };

const languageOptions: languageOption[] = [
	{
		language: 'English',
		code: 'en-US',
	},
	{ language: 'Magyar', code: 'hu' },
];

const LanguageSelector = () => {
	// Set the initial language from i18next's detected or default language
	const [language, setLanguage] = useState(i18next.language);

	const { i18n, t } = useTranslation();

	const handleLanguageChange = (e: SelectChangeEvent) => {
		const selectedLanguage = e.target.value;
		setLanguage(selectedLanguage);
		i18next.changeLanguage(selectedLanguage); // Update language in i18next
	};

	useEffect(() => {
		document.body.dir = i18n.dir(); // sets the body to ltr or rtl
	}, [i18n, i18n.language]);

	return (
		<FormControl margin="normal">
			<InputLabel
				id="language-selector"
				sx={{ color: 'white', '&.Mui-focused': { color: 'white' } }}
			>
				{t('language')}
			</InputLabel>
			<Select
				labelId="language-selector-label"
				id="language-selector"
				value={language}
				label="Language"
				onChange={handleLanguageChange}
				sx={{
					color: 'white',
					'& .MuiOutlinedInput-notchedOutline': {
						borderColor: 'white',
					},
					'&:hover .MuiOutlinedInput-notchedOutline': {
						borderColor: 'white',
					},
					'&.Mui-focused .MuiOutlinedInput-notchedOutline': {
						borderColor: 'white',
					},
					'& .MuiSvgIcon-root': {
						color: 'white',
					},
				}}
			>
				{languageOptions.map(({ language, code }, key) => (
					<MenuItem value={code} key={key}>
						{language}
					</MenuItem>
				))}
			</Select>
		</FormControl>
	);
};

export default LanguageSelector;
