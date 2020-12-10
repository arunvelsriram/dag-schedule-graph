import moment from 'moment';
import randomColor from 'randomcolor';

export const DATE_TIME_FORMAT = 'DD-MM-YYYY HH:mm:ss';
const BACKGROUND_COLOR_ALPHA = 0.5;
const BORDER_COLOR_ALPHA = 1;
const TRANSPARENT_COLOR = 'transparent';

function rgbaString(...rgba) {
    const params = rgba.join(', ');
    return `rgba(${params})`;
}

function getColors() {
    const rgb = randomColor({format: 'rgbArray'});
    const borderColor = rgbaString(...rgb, BORDER_COLOR_ALPHA);
    return {
        backgroundColor: rgbaString(...rgb, BACKGROUND_COLOR_ALPHA),
        borderColor: borderColor,
        hoverBackgroundColor: TRANSPARENT_COLOR,
        hoverBorderColor: borderColor,
    }
}

export function getDatasets(dagSchedules) {
    return Object.keys(dagSchedules).map((schedule, _index) => {
        const dagIds = dagSchedules[schedule];
        const dagCount = dagIds.length;
        const data = {x: parseFloat(schedule), y: dagCount, r: dagCount}
        const colors = getColors();
        return {
            label: dagIds,
            data: [data],
            ...colors
        }
    });
}

export function getXLabel(from, to) {
    const format = (timestamp) => moment(timestamp).format(DATE_TIME_FORMAT)
    return `Time - ${format(from)} to ${format(to)}`;
}
