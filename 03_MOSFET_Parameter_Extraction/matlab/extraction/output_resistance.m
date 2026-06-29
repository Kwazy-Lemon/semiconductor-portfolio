function ro = output_resistance(data)
%OUTPUT_RESISTANCE Extract MOSFET output resistance.
%
% Description:
%   Estimate the output resistance from the saturation region
%   of the output characteristics.
%
% Inputs:
%   data.VDS
%   data.IDS
%
% Outputs:
%   ro - Output resistance (Ohm)
%
% Author:
%   Jianhao Wu
%
% Project:
%   MOSFET Parameter Extraction Toolkit

%% Read Data

VDS = data.VDS;
IDS = data.IDS;

%% Linear Fit

p = polyfit(VDS, IDS, 1);

slope = p(1);

%% Output Resistance

ro = 1 / slope;

%% Display

fprintf("\n");
fprintf("=====================================\n");
fprintf(" Output Resistance Extraction\n");
fprintf("=====================================\n");
fprintf("ro = %.4e Ohm\n", ro);
fprintf("=====================================\n");

end


