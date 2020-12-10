import randomColor from 'randomcolor';
import moment from 'moment';
import {getDatasets, getXLabel} from '../chart-helper.js'

describe('getDatasets', () => {
    it('should return chart dataset', () => {
        const dagSchedules = {
            '1607644800000.0': ['test-dag-1', 'test-dag-2'],
            '1607644800001.0': ['test-dag-3', 'test-dag-4'],
            '1607644800002.0': ['test-dag-1']
        };
        randomColor.mockReturnValue([0, 0, 0])

        const actual = getDatasets(dagSchedules);

        expect(randomColor).toBeCalledWith({format: 'rgbArray'});
        const backgroundColor = 'rgba(0, 0, 0, 0.5)';
        const borderColor = 'rgba(0, 0, 0, 1)';
        const expected = [{
            label: ['test-dag-1', 'test-dag-2'],
            data: [{x: 1607644800000, y: 2, r: 2}],
            backgroundColor: backgroundColor,
            borderColor: borderColor,
            hoverBackgroundColor: 'transparent',
            hoverBorderColor: borderColor
        }, {
            label: ['test-dag-3', 'test-dag-4'],
            data: [{x: 1607644800001, y: 2, r: 2}],
            backgroundColor: backgroundColor,
            borderColor: borderColor,
            hoverBackgroundColor: 'transparent',
            hoverBorderColor: borderColor
        }, {
            label: ['test-dag-1'],
            data: [{x: 1607644800002, y: 1, r: 1}],
            backgroundColor: backgroundColor,
            borderColor: borderColor,
            hoverBackgroundColor: 'transparent',
            hoverBorderColor: borderColor
        }];
        expect(actual).toStrictEqual(expected);
    });
});

describe('getXLabel', () => {
    it('should construct x-axis label', () => {
        const fromTimestamp = moment('01012020 1530', 'DDMMYYYY HHmm').valueOf();
        const toTimestamp = moment('02012020 1530', 'DDMMYYYY HHmm').valueOf();

        const actual = getXLabel(fromTimestamp, toTimestamp);

        expect(actual).toBe('Time - 01-01-2020 15:30:00 to 02-01-2020 15:30:00');
    });
});
