function data = read_ltspice_csv(filename)
%READ_LTSPICE_CSV Import LTspice transfer curve.
%
% Author:
%   Jianhao Wu

fprintf('=========================================\n');
fprintf(' MOSFET Parameter Extraction Toolkit\n');
fprintf(' LTspice Data Import\n');
fprintf('=========================================\n');

T = readtable(filename);

data.VGS = T{:,1};
data.IDS = T{:,2};

data.ColumnNames = T.Properties.VariableNames;
data.RawTable = T;

fprintf('Import completed.\n');
fprintf('Samples : %d\n',length(data.VGS));

end
