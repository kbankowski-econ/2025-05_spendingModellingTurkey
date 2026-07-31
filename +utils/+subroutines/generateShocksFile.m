function generateShocksFile(fileName, shockSpecs)
    % Write the full body of a Dynare shocks block to fileName.
    %
    % The generated file is meant to be the sole content of a model's
    % shocks block:   shocks; @#include "<model>.shockValues" end;
    %
    % Inputs:
    %   fileName   - name of the output file (string)
    %   shockSpecs - cell array of shock specs, each a cell:
    %                {varName, kind, value, periods[, valueFormat]}
    %                kind 'const'  - constant value over the periods range,
    %                                e.g. '1:1000' or '40:1000'
    %                kind 'ramp'   - linear increase from 0 to value over
    %                                the quarters in '1:N', then held
    %                                constant through period 1000
    %                kind 'ar1'    - AR(1)-decaying path: value is a two-element
    %                                vector [impact, rho]; the shock follows
    %                                impact * rho.^(0:N-1) over the quarters in
    %                                '1:N' (periods enumerated individually so
    %                                each quarter gets its own value). rho = 0
    %                                is a single-period shock; rho -> 1 is
    %                                effectively permanent.
    %                kind 'custom' - explicit values vector, periods string
    %                                written verbatim
    %                valueFormat   - sprintf format for the values; default
    %                                '%g'. Use 'roundtrip' for the shortest
    %                                decimal that parses back to the exact
    %                                double, where the historical shock
    %                                values carried full precision.

    fid = fopen(fileName, 'w');

    for k = 1:numel(shockSpecs)
        spec = shockSpecs{k};
        [varName, kind, value, periods] = spec{1:4};
        if numel(spec) >= 5
            valueFormat = spec{5};
        else
            valueFormat = '%g';
        end
        fprintf(fid, 'var %s;\n', varName);

        switch kind
            case 'const'
                fprintf(fid, 'periods %s ;\n', periods);
                writeValues(fid, value, valueFormat);

            case 'ramp'
                bounds = sscanf(periods, '%d:%d');
                assert(bounds(1) == 1, 'generateShocksFile:ramp', ...
                       'ramps must start at period 1');
                numQuarters = bounds(2);
                fprintf(fid, 'periods ');
                fprintf(fid, '%d ', 1:numQuarters);
                fprintf(fid, '%d:1000 ;\n', numQuarters + 1);
                increment = value / numQuarters;
                writeValues(fid, [(1:numQuarters) * increment, value], valueFormat);

            case 'ar1'
                bounds = sscanf(periods, '%d:%d');
                assert(bounds(1) == 1, 'generateShocksFile:ar1', ...
                       'ar1 paths must start at period 1');
                numQuarters = bounds(2);
                impact = value(1);
                rho    = value(2);
                seq = impact * rho .^ (0:numQuarters - 1);
                fprintf(fid, 'periods ');
                fprintf(fid, '%d ', 1:numQuarters);
                fprintf(fid, ';\n');
                writeValues(fid, seq, valueFormat);

            case 'custom'
                fprintf(fid, 'periods %s ;\n', periods);
                writeValues(fid, value, valueFormat);

            otherwise
                error('generateShocksFile:kind', 'Unknown shock kind "%s".', kind);
        end
    end

    fclose(fid);

    fprintf('Shocks file "%s" generated successfully.\n', fileName);
end

function writeValues(fid, values, valueFormat)
    % Write the values section, one value per line.
    fprintf(fid, 'values\n');
    for i = 1:numel(values)
        if strcmp(valueFormat, 'roundtrip')
            % shortest decimal that parses back to the exact double
            for precision = 1:17
                valueText = sprintf('%.*g', precision, values(i));
                if str2double(valueText) == values(i)
                    break
                end
            end
        else
            valueText = sprintf(valueFormat, values(i));
        end
        fprintf(fid, '    %s\n', valueText);
    end
    fprintf(fid, ';\n');
end
