function mu = mobility(data, method)
%MOBILITY Extract effective carrier mobility.
%
% Description:
%   Estimate effective carrier mobility from MOSFET transfer
%   characteristics.
%
% Inputs:
%   data    - Structure containing MOSFET I-V data
%   method  - Extraction method
%             "analytical"
%             "regression"
%
% Outputs:
%   mu      - Effective carrier mobility (cm^2/V·s)
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
    method = "analytical";
end

%% Read Data

VGS = data.VGS;
IDS = data.IDS;

%% Select Method

switch lower(method)

    case "analytical"

        % To be implemented
        mu = [];

    case "regression"

        % To be implemented
        mu = [];

    otherwise

        error("Unknown mobility extraction method.");

end

end
