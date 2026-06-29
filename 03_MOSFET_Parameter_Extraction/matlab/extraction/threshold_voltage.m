function Vth = threshold_voltage(data,method)
%THRESHOLD_VOLTAGE Extract MOSFET threshold voltage.
%
% Description:
%   Estimate the threshold voltage from transfer characteristics.
%
% Inputs:
%   data   - Structure containing VGS and IDS
%   method - Extraction method
%
%            "linear" (default)
%
% Outputs:
%   Vth - Threshold voltage (V)
%
% Author:
%   Jianhao Wu
%
% Version:
%   v1.0

if nargin < 2
    method = "linear";
end

switch lower(method)

    case "linear"

        Vth = linear_extraction(data);

    case "constant"

        Vth = constant_current(data);

    otherwise

        error("Unknown extraction method.");

end

end
