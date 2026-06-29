function data = read_ltspice_csv(filename)
%READ_LTSPICE_CSV Import LTspice simulation data.
%
% Description:
%   Reads LTspice exported TXT/CSV files and converts them into a MATLAB
%   structure for parameter extraction and visualization.
%
% Inputs:
%   filename - LTspice output file
%
% Outputs:
%   data - Structure containing imported data
%
% Fields:
%   data.X
%   data.Y
%   data.RawTable
%
% Author:
%   Jianhao Wu
%
% Project:
%   MOSFET Parameter Extraction Toolkit

fprintf('-----------------------------------------\n');
fprintf(' MOSFET Parameter Extraction Toolkit\n');
fprintf(' LTspice Data Import Module\n');
fprintf('-----------------------------------------\n');

% Read table
T = readtable(filename);

% Store original table
data.RawTable = T;

% First column
data.X = T{:,1};

% Second column
data.Y = T{:,2};

% Column names
data.ColumnNames = T.Properties.VariableNames;

fprintf('Import Successful!\n');
fprintf('Samples : %d\n',height(T));
fprintf('Columns : %d\n',width(T));

end
