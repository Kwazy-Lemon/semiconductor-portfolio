function ro = output_resistance(data, method)
%OUTPUT_RESISTANCE Estimate output resistance.
%
% Description:
%   Estimate MOSFET output resistance from saturation-region
%   output characteristics.
%
% Inputs:
%   data
%   method
%       "linear"
%       "analytical"
%
% Outputs:
%   ro
%
% Author:
%   Jianhao Wu
%
% Repository:
%   MOSFET Parameter Extraction Toolkit
%
% Version:
%   v1.0

%% Default Method

if nargin < 2
    method = "linear";
end

%% Read Data

VDS = data.VDS;
IDS = data.IDS;

%% Select Method

switch lower(method)

    case "linear"

        % To be implemented
        ro = [];

    case "analytical"

        % To be implemented
        ro = [];

    otherwise

        error("Unknown output resistance estimation method.");

end

end
