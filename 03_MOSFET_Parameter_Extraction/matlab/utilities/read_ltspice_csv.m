function data = read_ltspice_csv(filename)
%READ_LTSPICE_CSV Import LTspice datasets.
%
% Description:
%   Import LTspice simulation data for MOSFET parameter extraction.
%
% Inputs:
%   filename - Path to LTspice output file
%
% Outputs:
%   data - Structure containing imported data
%
% Author:
%   Jianhao Wu
%
% Project:
%   MOSFET Parameter Extraction Toolkit

fprintf("=========================================\n");
fprintf(" MOSFET Parameter Extraction Toolkit\n");
fprintf(" LTspice Data Import\n");
fprintf("=========================================\n");

T = readtable(filename,'VariableNamingRule','preserve');

data = struct();

%% Save Raw Table

data.RawTable = T;
data.ColumnNames = T.Properties.VariableNames;

%% Detect Dataset Type

[~,name,~] = fileparts(filename);

switch lower(name)

    case "id_vgs"

        data.Type = "Transfer";

        data.VGS = T{:,1};
        data.IDS = T{:,2};

    case "id_vds"

        data.Type = "Output";

        data.VDS = T{:,1};
        data.IDS = T{:,2};

    otherwise

        error("Unsupported LTspice dataset.");

end

fprintf("Import completed.\n");

fprintf("Dataset : %s\n",data.Type);

fprintf("Samples : %d\n",height(T));

fprintf("=========================================\n");

end
