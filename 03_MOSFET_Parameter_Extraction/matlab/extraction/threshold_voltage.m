function Vth = threshold_voltage(data,method)
%THRESHOLD_VOLTAGE Extract MOSFET threshold voltage.
%
% Description:
%   Estimate the threshold voltage from transfer characteristics.
%
% Inputs:
%   data    - Structure containing VGS and IDS
%   method  - Extraction method
%
%             "linear"  (default)
%             "constant_current"
%
% Outputs:
%   Vth     - Threshold voltage (V)
%
% Author:
%   Jianhao Wu
%
% Project:
%   MOSFET Parameter Extraction Toolkit
%
% Version:
%   v1.0


if nargin < 2
    method = "linear";
end


fprintf("\n");
fprintf("=====================================\n");
fprintf("Threshold Voltage Extraction\n");
fprintf("=====================================\n");

switch lower(method)

    case "linear"

        [Vth,fit] = linear_extraction(data);

    case "constant_current"

        Vth = constant_current(data);

        fit = [];

    otherwise

        error("Unknown extraction method.");

end

assignin('base','fit',fit);

fprintf("Method : %s\n",method);
fprintf("Vth    : %.4f V\n",Vth);
fprintf("=====================================\n");

end
