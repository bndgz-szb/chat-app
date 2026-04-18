import { useTranslation } from 'react-i18next';

function LoadingDiv() {
	const { t } = useTranslation();
	return <div>{t('loading')}</div>;
}
export default LoadingDiv;
