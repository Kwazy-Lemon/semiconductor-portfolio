function data = read_ltspice_csv(filename)
%READ_LTSPICE_CSV Import LTspice stepped simulation data.
%
% Description:
%   Read LTspice output files containing stepped simulations
%   (e.g. VGS sweep with VDS curves).
%
% Inputs:
%   filename - LTspice exported text/csv file
%
% Outputs:
%   data - Structure containing:
%          data.VGS
%          data.VDS
%          data.IDS
%
% Author:
%   Jianhao Wu
%
% Repository:
%   MOSFET Parameter Extraction Toolkit
%
% Version:
%   v1.0

%% Open File

fid = fopen(filename,'r');

if fid==-1
    error('Cannot open file.');
end

%% Read All Lines

lines = {};

while ~feof(fid)

    lines{end+1} = fgetl(fid);

end

fclose(fid);

%% Initialize

VGS = [];
VDS = {};
IDS = {};

curve = 0;

%% Parse File

for i = 1:length(lines)

    line = strtrim(lines{i});

    % Skip empty line
    if isempty(line)
        continue;
    end

    % Detect Step Information
    if contains(line,'Step Information')

        curve = curve + 1;

        token = regexp(line,'V1=([-\d\.Ee+]+)','tokens');

        if ~isempty(token)

            VGS(curve) = str2double(token{1}{1});

        end

        VDS{curve} = [];
        IDS{curve} = [];

        continue;

    end

    % Skip header
    if startsWith(line,'V2')
        continue;
    end

    % Read numeric data
    value = sscanf(line,'%f %f');

    if numel(value)==2

        VDS{curve}(end+1,1) = value(1);
        IDS{curve}(end+1,1) = value(2);

    end

end

%% Store Data

data = struct();

data.VGS = VGS;
data.VDS = VDS;
data.IDS = IDS;

end
